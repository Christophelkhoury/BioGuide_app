#Projet : BioGuide
#Auteurs : Christophe El Khoury, Tia Kahil, Alaa Hamdan
"""Moteur de recherche TF-IDF sur les passages indexés."""
import re
import sqlite3
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import List, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from src.db import connect, init_fts, DB_PATH

_MIN_CONTENT_LEN = 60
_THERAPEUTIC_KEYWORDS = (
    "remède", "traitement", "usage", "contre", "préparer", "fébrifuge",
    "plante", "infusion", "décoction", "teinture", "soigner", "guérir",
    "maladie", "symptôme", "appliquer", "prendre", "dose", "posologie",
)


def _normalize_query(q: str) -> str:
    """Normalise la requête (minuscules, sans accents)."""
    q = q.lower().strip()
    nfd = unicodedata.normalize("NFD", q)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def _strip_metadata(text: str) -> str:
    """Retire les métadonnées type JSON pour estimer la longueur utile."""
    if not text:
        return ""
    t = re.sub(r',\s*"[^"]*OCR[^"]*"\s*:\s*"[^"]*"', ' ', text, flags=re.IGNORECASE)
    t = re.sub(r',\s*"[a-zA-Z]+"\s*:\s*"[^"]*"', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def _word_boundary_match(word: str, text: str) -> bool:
    """True if `word` appears in `text` as a complete word (not a substring)."""
    if not word or not text:
        return False
    return bool(re.search(r"\b" + re.escape(word) + r"\b", text))


def _therapeutic_bonus(text: str) -> float:
    """Bonus de score si le passage contient des termes liés aux remèdes."""
    if not text:
        return 0.0
    lower = text.lower()
    return 1.0 if any(_word_boundary_match(kw, lower) for kw in _THERAPEUTIC_KEYWORDS) else 0.0


def _passage_contains_query(text: str, query: str) -> bool:
    """Indique si au moins un mot de la requête est présent dans le passage."""
    words = _normalize_query(query).split()
    if not words:
        return False
    text_norm = _normalize_query(text)
    return any(_word_boundary_match(w, text_norm) for w in words)


def _rank_and_balance(
    results: List[Tuple[str, int, str, float]],
    top_k: int,
    book_filter: Optional[str],
) -> List[Tuple[str, int, str, float]]:
    """Trie et équilibre les résultats entre les ouvrages."""
    results = sorted(
        results,
        key=lambda r: (_therapeutic_bonus(r[2]) > 0, r[3]),
        reverse=True,
    )
    if book_filter or top_k <= 0:
        return results[:top_k]
    by_book = defaultdict(list)
    for r in results:
        by_book[r[0]].append(r)
    book_order = list(by_book.keys())
    balanced = []
    indices = {b: 0 for b in book_order}
    while len(balanced) < top_k:
        got = 0
        for book_id in book_order:
            if len(balanced) >= top_k:
                break
            idx = indices[book_id]
            if idx < len(by_book[book_id]):
                balanced.append(by_book[book_id][idx])
                indices[book_id] = idx + 1
                got += 1
        if got == 0:
            break
    return balanced[:top_k]


def _fts_get_candidates(
    query: str, book_filter: Optional[str], limit: int
) -> List[Tuple[int, str, int]]:
    """Candidats FTS5 pour la requête (identifiant passage, livre, page)."""
    raw_words = [w for w in query.lower().strip().split() if len(w) >= 2]
    norm_words = _normalize_query(query).split()
    terms_set = set(raw_words) | set(w for w in norm_words if len(w) >= 2)
    if not terms_set:
        return []
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM passages_fts")
        if cur.fetchone()[0] == 0:
            conn.close()
            init_fts()
            conn = connect()
            cur = conn.cursor()
    except Exception:
        conn.close()
        return []
    terms = []
    for w in terms_set:
        safe = w.replace('"', '""')
        terms.append(f'"{safe}"')
    match_expr = " OR ".join(terms)
    try:
        cur.execute(
            "SELECT rowid FROM passages_fts WHERE passages_fts MATCH ? LIMIT ?",
            (match_expr, limit),
        )
        rowids = [row[0] for row in cur.fetchall()]
    except Exception:
        conn.close()
        return []
    if not rowids:
        conn.close()
        return []
    placeholders = ",".join("?" * len(rowids))
    cur.execute(
        f"SELECT passage_id, book_id, page FROM passages WHERE passage_id IN ({placeholders})",
        rowids,
    )
    rows = cur.fetchall()
    if book_filter:
        rows = [(pid, bid, p) for pid, bid, p in rows if bid == book_filter]
    conn.close()
    return rows


def _sql_fallback_search(
    query: str, top_k: int, book_filter: Optional[str]
) -> List[Tuple[str, int, str, float]]:
    """Recherche de secours par balayage SQL et filtrage sur les mots normalisés."""
    conn = connect()
    cur = conn.cursor()
    words = _normalize_query(query).split()
    if not words:
        conn.close()
        return []
    if book_filter:
        cur.execute(
            "SELECT book_id, page, text FROM passages WHERE book_id = ?",
            (book_filter,),
        )
    else:
        cur.execute("SELECT book_id, page, text FROM passages")
    rows = cur.fetchall()
    conn.close()
    results = []
    seen = set()
    for book_id, page, text in rows:
        key = (book_id, page, hash(text[:80]))
        if key in seen:
            continue
        content = _strip_metadata(text)
        if len(content) < _MIN_CONTENT_LEN:
            continue
        if not _passage_contains_query(text, query):
            continue
        text_norm = _normalize_query(text)
        score = sum(1.0 for w in words if _word_boundary_match(w, text_norm))
        score = score / max(len(words), 1) + 0.2 * _therapeutic_bonus(text)
        seen.add(key)
        results.append((book_id, page, text, score))
    return _rank_and_balance(results, top_k, book_filter)


class SearchEngine:
    """Moteur de recherche hybride (FTS5, TF-IDF, secours SQL)."""

    def __init__(self):
        """Initialise les attributs du moteur avant construction d'index."""
        self.vectorizer = None
        self.passage_matrix = None
        self.passage_ids: List[Tuple[str, int, int]] = []
        self.book_filter: Optional[str] = None

    def build_index(self, book_filter: Optional[str] = None):
        """Construit la matrice TF-IDF à partir des passages en base."""
        self.book_filter = book_filter
        conn = connect()
        cur = conn.cursor()
        
        if book_filter:
            cur.execute(
                "SELECT passage_id, book_id, page, text FROM passages WHERE book_id = ?",
                (book_filter,)
            )
        else:
            cur.execute("SELECT passage_id, book_id, page, text FROM passages")
        
        passages = cur.fetchall()
        conn.close()
        
        if not passages:
            print(f"Warning: No passages found for book_filter={book_filter}")
            return
        
        texts = [p[3] for p in passages]
        self.passage_ids = [(p[1], p[2], p[0]) for p in passages]

        self.vectorizer = TfidfVectorizer(
            max_features=None,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            stop_words=None,
            lowercase=True,
            strip_accents="unicode",
            token_pattern=r"(?u)\b\w+\b",
        )
        
        try:
            self.passage_matrix = self.vectorizer.fit_transform(texts)
        except Exception:
            self.vectorizer = TfidfVectorizer(
                max_features=None,
                ngram_range=(1, 1),
                min_df=1,
                max_df=0.95,
                lowercase=True,
                strip_accents="unicode",
            )
            self.passage_matrix = self.vectorizer.fit_transform(texts)
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[str, int, str, float]]:
        """Retourne les passages les plus pertinents pour la requête."""
        query = (query or "").strip()
        if not query:
            return []

        fts_candidates = _fts_get_candidates(query, self.book_filter, limit=top_k * 10)
        if fts_candidates:
            conn = connect()
            cur = conn.cursor()
            results = []
            seen = set()
            for passage_id, book_id, page in fts_candidates:
                cur.execute("SELECT text FROM passages WHERE passage_id = ?", (passage_id,))
                row = cur.fetchone()
                if not row:
                    continue
                text = row[0]
                if len(_strip_metadata(text)) < _MIN_CONTENT_LEN:
                    continue
                if not _passage_contains_query(text, query):
                    continue
                key = (book_id, page, hash(text[:80]))
                if key in seen:
                    continue
                seen.add(key)
                words = _normalize_query(query).split()
                text_norm = _normalize_query(text)
                score = sum(1.0 for w in words if _word_boundary_match(w, text_norm))
                score = score / max(len(words), 1) + 0.2 * _therapeutic_bonus(text)
                results.append((book_id, page, text, score))
            conn.close()
            if results:
                return _rank_and_balance(results, top_k, self.book_filter)

        if self.vectorizer is not None and self.passage_matrix is not None:
            query_normalized = _normalize_query(query)
            query_vec = self.vectorizer.transform([query_normalized])
            similarities = cosine_similarity(query_vec, self.passage_matrix).flatten()
            top_indices = np.argsort(similarities)[::-1][:top_k * 8]
            conn = connect()
            cur = conn.cursor()
            results = []
            seen = set()
            for idx in top_indices:
                if similarities[idx] <= 0:
                    continue
                book_id, page, passage_id = self.passage_ids[idx]
                cur.execute("SELECT text FROM passages WHERE passage_id = ?", (passage_id,))
                row = cur.fetchone()
                if not row:
                    continue
                text = row[0]
                if len(_strip_metadata(text)) < _MIN_CONTENT_LEN:
                    continue
                if not _passage_contains_query(text, query):
                    continue
                key = (book_id, page, hash(text[:80]))
                if key in seen:
                    continue
                seen.add(key)
                base_score = float(similarities[idx])
                bonus = 0.2 * _therapeutic_bonus(text)
                results.append((book_id, page, text, base_score + bonus))
                if len(results) >= top_k * 4:
                    break
            conn.close()
            if results:
                return _rank_and_balance(results, top_k, self.book_filter)

        return _sql_fallback_search(query, top_k, self.book_filter)


def get_search_engine(book_filter: Optional[str] = None):
    """Instancie un moteur prêt à l'emploi avec index construit."""
    engine = SearchEngine()
    engine.build_index(book_filter)
    return engine

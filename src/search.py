"""
TF-IDF search engine for passages.
"""
import re
import sqlite3
import unicodedata
from pathlib import Path
from typing import List, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from src.db import connect, DB_PATH

# Minimum content length (after stripping metadata) to keep a passage
_MIN_CONTENT_LEN = 60
# Keywords that suggest a passage contains remedies/treatments (relevance bonus)
_THERAPEUTIC_KEYWORDS = (
    "remède", "traitement", "usage", "contre", "préparer", "fébrifuge",
    "plante", "infusion", "décoction", "teinture", "soigner", "guérir",
    "maladie", "symptôme", "appliquer", "prendre", "dose", "posologie",
)


def _normalize_query(q: str) -> str:
    """Normalize query: lowercase and strip accents (so 'fievre' matches 'fièvre')."""
    q = q.lower().strip()
    # Remove accents for matching
    nfd = unicodedata.normalize("NFD", q)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def _strip_metadata(text: str) -> str:
    """Remove JSON-like Gallica/OCR metadata to get content length."""
    if not text:
        return ""
    t = re.sub(r',\s*"[^"]*OCR[^"]*"\s*:\s*"[^"]*"', ' ', text, flags=re.IGNORECASE)
    t = re.sub(r',\s*"[a-zA-Z]+"\s*:\s*"[^"]*"', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def _therapeutic_bonus(text: str) -> float:
    """Return 1.0 if passage contains therapeutic/solution-oriented terms."""
    if not text:
        return 0.0
    lower = text.lower()
    return 1.0 if any(kw in lower for kw in _THERAPEUTIC_KEYWORDS) else 0.0


def _sql_fallback_search(
    query: str, top_k: int, book_filter: Optional[str]
) -> List[Tuple[str, int, str, float]]:
    """
    Fallback: when TF-IDF returns nothing, fetch passages and filter in Python
    using normalized text so "fievre" matches "fièvre".
    """
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
        text_norm = _normalize_query(text)
        score = 0.0
        for w in words:
            if w in text_norm:
                score += 1.0
        if score > 0:
            seen.add(key)
            score = score / max(len(words), 1) + 0.2 * _therapeutic_bonus(text)
            results.append((book_id, page, text, score))
    
    results.sort(key=lambda x: x[3], reverse=True)
    return results[:top_k]


class SearchEngine:
    """TF-IDF search engine for passages."""
    
    def __init__(self):
        self.vectorizer = None
        self.passage_matrix = None
        self.passage_ids: List[Tuple[str, int, int]] = []  # (book_id, page, passage_id)
        self.book_filter: Optional[str] = None
    
    def build_index(self, book_filter: Optional[str] = None):
        """Build TF-IDF index from database passages."""
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
        
        # No max_features limit so no word is dropped (e.g. "fièvre" must be in vocabulary)
        # Use analyzer that splits on non-letters so French words are kept
        self.vectorizer = TfidfVectorizer(
            max_features=None,  # Keep all terms so "fievre"/"fièvre" is never dropped
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            stop_words=None,
            lowercase=True,
            strip_accents="unicode",  # fièvre -> fievre in vocabulary
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
        """
        Search for passages matching the query.
        Uses TF-IDF first; if no results, falls back to SQL LIKE search.
        """
        query = (query or "").strip()
        if not query:
            return []
        
        # 1) Try TF-IDF
        if self.vectorizer is not None and self.passage_matrix is not None:
            query_normalized = _normalize_query(query)
            query_vec = self.vectorizer.transform([query_normalized])
            similarities = cosine_similarity(query_vec, self.passage_matrix).flatten()
            # Get more candidates so we can filter and re-rank
            top_indices = np.argsort(similarities)[::-1][:top_k * 6]
            conn = connect()
            cur = conn.cursor()
            results = []
            seen_passages = set()
            
            for idx in top_indices:
                if similarities[idx] <= 0:
                    continue
                book_id, page, passage_id = self.passage_ids[idx]
                cur.execute("SELECT text FROM passages WHERE passage_id = ?", (passage_id,))
                row = cur.fetchone()
                if not row:
                    continue
                text = row[0]
                # Skip passages that are mostly metadata (too short after strip)
                content = _strip_metadata(text)
                if len(content) < _MIN_CONTENT_LEN:
                    continue
                text_hash = hash(text[:100] + str(len(text)))
                passage_key = (book_id, page, text_hash)
                if passage_key in seen_passages:
                    continue
                seen_passages.add(passage_key)
                base_score = float(similarities[idx])
                bonus = 0.2 * _therapeutic_bonus(text)
                results.append((book_id, page, text, base_score + bonus))
                if len(results) >= top_k * 2:
                    break
            
            conn.close()
            results.sort(key=lambda x: x[3], reverse=True)
            results = results[:top_k]
            
            if results:
                return results
        
        # 2) Fallback: SQL search (e.g. when term was not in TF-IDF vocabulary or index empty)
        return _sql_fallback_search(query, top_k, self.book_filter)


def get_search_engine(book_filter: Optional[str] = None):
    """Get search engine instance."""
    engine = SearchEngine()
    engine.build_index(book_filter)
    return engine

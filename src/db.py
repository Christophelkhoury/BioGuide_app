"""Connexion SQLite et schéma des livres et passages indexés."""
import sqlite3
from pathlib import Path

DB_PATH = Path("phyto.db")

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS books (
  book_id TEXT PRIMARY KEY,
  title   TEXT NOT NULL,
  ark     TEXT NOT NULL,
  source_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS passages (
  passage_id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id TEXT NOT NULL,
  page INTEGER NOT NULL,
  text TEXT NOT NULL,
  FOREIGN KEY(book_id) REFERENCES books(book_id)
);

CREATE INDEX IF NOT EXISTS idx_passages_book_page ON passages(book_id, page);
"""


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Ouvre une connexion à la base avec clés étrangères activées."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Path = DB_PATH) -> None:
    """Crée les tables books et passages si elles n'existent pas."""
    conn = connect(db_path)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()

def upsert_book(book_id: str, title: str, ark: str, source_url: str, db_path: Path = DB_PATH) -> None:
    conn = connect(db_path)
    conn.execute(
        "INSERT OR REPLACE INTO books(book_id, title, ark, source_url) VALUES (?,?,?,?)",
        (book_id, title, ark, source_url),
    )
    conn.commit()
    conn.close()


def insert_passage(book_id: str, page: int, text: str, db_path: Path = DB_PATH) -> None:
    """Ajoute un passage de texte pour une page donnée."""
    conn = connect(db_path)
    conn.execute(
        "INSERT INTO passages(book_id, page, text) VALUES (?,?,?)",
        (book_id, page, text),
    )
    conn.commit()
    conn.close()


FTS5_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS passages_fts USING fts5(text, content='passages', content_rowid='passage_id', tokenize='unicode61');

CREATE TRIGGER IF NOT EXISTS passages_ai AFTER INSERT ON passages BEGIN
  INSERT INTO passages_fts(rowid, text) VALUES (new.passage_id, new.text);
END;
CREATE TRIGGER IF NOT EXISTS passages_ad AFTER DELETE ON passages BEGIN
  INSERT INTO passages_fts(passages_fts, rowid) VALUES ('delete', old.passage_id);
END;
CREATE TRIGGER IF NOT EXISTS passages_au AFTER UPDATE ON passages BEGIN
  INSERT INTO passages_fts(passages_fts, rowid) VALUES ('delete', old.passage_id);
  INSERT INTO passages_fts(rowid, text) VALUES (new.passage_id, new.text);
END;
"""


def init_fts(db_path: Path = DB_PATH) -> None:
    """Initialise la table FTS5 et synchronise les passages existants."""
    conn = connect(db_path)
    conn.executescript(FTS5_SCHEMA)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM passages_fts")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO passages_fts(rowid, text) SELECT passage_id, text FROM passages")
    conn.commit()
    conn.close()

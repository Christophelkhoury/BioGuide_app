#Projet : BioGuide
#Auteurs : Christophe El Khoury, Tia Kahil, Alaa Hamdan
"""Import des textes Gallica dans la base SQLite locale."""
from lxml import html as lhtml

from src.db import connect, init_db, init_fts, upsert_book
from src.clean_text import clean_ocr_text, split_into_passages
from src.gallica_fetch import fetch_texteimage_html, get_last_page

BOOKS = [
    {
        "book_id": "plantes",
        "title": "La santé par les plantes",
        "ark_id": "bpt6k5688257m",
        "source_url": "https://gallica.bnf.fr/ark:/12148/bpt6k5688257m",
    },
    {
        "book_id": "pauvres",
        "title": "Le médecin des pauvres",
        "ark_id": "bpt6k5791358q",
        "source_url": "https://gallica.bnf.fr/ark:/12148/bpt6k5791358q",
    },
]

def html_to_text(page_html: str) -> str:
    """Extrait le texte brut d'une page HTML."""
    doc = lhtml.fromstring(page_html)
    return " ".join(doc.text_content().split())

def main():
    """Parcourt les ouvrages définis dans BOOKS et remplit phyto.db."""
    init_db()
    init_fts()

    conn = connect()
    cur = conn.cursor()

    for b in BOOKS:
        print(f"\n==> Import: {b['title']} ({b['ark_id']})")
        upsert_book(b["book_id"], b["title"], b["ark_id"], b["source_url"])

        last_page = get_last_page(b["ark_id"])
        print(f"Dernière page détectée: {last_page}")

        imported_pages = 0

        for page in range(1, last_page + 1):
            raw_html = fetch_texteimage_html(b["ark_id"], page)
            if raw_html is None:
                continue

            text = html_to_text(raw_html)
            text = clean_ocr_text(text)

            if len(text) < 300:
                continue

            passages = [(b["book_id"], page, pas) for pas in split_into_passages(text)]
            if passages:
                cur.executemany(
                    "INSERT INTO passages(book_id, page, text) VALUES (?,?,?)",
                    passages
                )
                conn.commit()

            imported_pages += 1
            if imported_pages % 25 == 0:
                print(f"  pages importées: {imported_pages}/{last_page}")

        print(f"OK: pages réellement importées = {imported_pages}")

    conn.close()
    print("\nTerminé. Base: phyto.db")

if __name__ == "__main__":
    main()

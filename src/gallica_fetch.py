"""Téléchargement des vues « texte + image » Gallica."""
import requests

BASE_TXTIMG = "https://gallica.bnf.fr/ark:/12148/{ark_id}/f{page}.item.texteImage"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_texteimage_html(ark_id: str, page: int, timeout: int = 25) -> str | None:
    """Récupère le HTML de la page numérique ou None si indisponible."""
    url = BASE_TXTIMG.format(ark_id=ark_id, page=page)
    r = requests.get(url, timeout=timeout, headers=HEADERS)
    if r.status_code != 200:
        return None
    h = r.text
    if "texteImage" not in h and "Texte" not in h and len(h) < 800:
        return None
    return h

def get_last_page(ark_id: str, max_pages: int = 800) -> int:
    """Détermine le dernier numéro de page accessible pour un ark Gallica."""
    last_ok = 0
    fails = 0
    for p in range(1, max_pages + 1):
        h = fetch_texteimage_html(ark_id, p)
        if h is None:
            fails += 1
            if fails >= 20:
                break
        else:
            fails = 0
            last_ok = p
    if last_ok == 0:
        raise RuntimeError("Aucune page détectée (teste manuellement f1.item.texteImage).")
    return last_ok

#Projet : BioGuide
#Auteurs : Christophe El Khoury, Tia Kahil, Alaa Hamdan
"""Nettoyage de texte OCR et découpage en passages."""
import re


def clean_ocr_text(t: str) -> str:
    """Normalise espaces et ponctuation après OCR."""
    t = t.replace("\u00ad", "")
    t = re.sub(r"\s+", " ", t).strip()
    t = t.replace(" ,", ",").replace(" .", ".")
    return t

def split_into_passages(t: str, min_len: int = 180) -> list[str]:
    """Découpe le texte en blocs d'environ min_len caractères."""
    sentences = re.split(r"(?<=[\.\?\!;])\s+", t)
    passages, buff, size = [], [], 0
    for s in sentences:
        if not s.strip():
            continue
        buff.append(s.strip())
        size += len(s)
        if size >= min_len:
            passages.append(" ".join(buff))
            buff, size = [], 0
    if buff:
        passages.append(" ".join(buff))
    return passages

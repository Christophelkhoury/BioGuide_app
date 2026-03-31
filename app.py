#Projet : BioGuide
#Auteurs : Christophe El Khoury, Tia Kahil, Alaa Hamdan
"""Entrée Streamlit Cloud (racine) — charge sources/ dans sys.path puis sources/main.py."""
from pathlib import Path
import runpy
import sys

_root = Path(__file__).resolve().parent
_sources = _root / "sources"
if str(_sources) not in sys.path:
    sys.path.insert(0, str(_sources))

runpy.run_path(str(_sources / "main.py"), run_name="__main__")

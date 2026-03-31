#Projet : BioGuide
#Auteurs : Christophe El Khoury, Tia Kahil, Alaa Hamdan
"""Entrée Streamlit Cloud — délègue à main.py (point d'entrée réel)."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parent / "main.py"), run_name="__main__")

# BioGuide

Streamlit + SQLite autour de deux livres Gallica (médecine populaire, plantes).  
La page d’accueil résume ce qui est indexé ; une partie du site permet de poser des questions sur le fond textuel (recherche + synthèse, avec clé API dans les secrets).

## Contenu du dépôt (Trophées NSI)

- `présentation.md` — présentation du projet  
- `licence.txt` — licences du code et des textes  
- `requirements.txt` — dépendances Python  
- `sources/` — code source (point d’entrée : `sources/main.py`)  
- `sources/pages/` — pages Streamlit  
- `sources/src/` — base de données, recherche (FTS / TF-IDF), appels au modèle de langage  
- `sources/import_gallica.py` — régénérer la base (long, à lancer en local si besoin)  
- `data/phyto.db` — base SQLite (via **Git LFS**, ~450 Mo ; sans LFS le clone n’a qu’un pointeur)  
- `test/` — script de test optionnel de la clé API  

## Contraintes

- **Python** : 3.10 ou supérieur (3.12 recommandé).  
- **Git LFS** : nécessaire pour récupérer le fichier `data/phyto.db` en taille réelle.

## Installation

Prérequis : Python 3.10+, [Git LFS](https://git-lfs.com).

```bash
git clone https://github.com/Christophelkhoury/BioGuide_app.git
cd BioGuide_app
git lfs pull
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
```

Éditer `.streamlit/secrets.toml` : renseigner la clé (voir l’exemple).

Lancer l’application **depuis la racine du dépôt** :

```bash
streamlit run sources/main.py
```

(Sous Linux/macOS, adaptez l’activation du venv : `source venv/bin/activate`.)

## Streamlit Cloud

Fichier principal recommandé : `sources/main.py`.  
Si le tableau de bord pointe encore vers `app.py`, utiliser `sources/app.py` (délègue à `main.py`).  
Ne pas commiter `secrets.toml` (déjà ignoré) ; copier les clés dans l’onglet **Secrets** du tableau de bord Streamlit.

```toml
OPENAI_API_KEY = "…"
```

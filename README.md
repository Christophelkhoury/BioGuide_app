# BioGuide

Streamlit + SQLite autour de deux livres Gallica (médecine populaire, plantes).  
La page d’accueil résume ce qui est indexé ; une partie du site permet de poser des questions sur le fond textuel (recherche + synthèse, avec clé API dans les secrets).

## Contenu du dépôt

- `main.py` — entrée Streamlit  
- `pages/` — les autres écrans  
- `src/` — base de données, recherche (FTS / TF-IDF), appels au modèle de langage  
- `import_gallica.py` — régénérer `phyto.db` (long, à lancer en local si besoin)  
- `phyto.db` — via **Git LFS** (~450 Mo), sinon le clone n’a qu’un pointeur

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

Lancer :

```bash
streamlit run main.py
```

## Streamlit Cloud

Fichier principal : `main.py` (recommandé dans les paramètres de l’app).  
Si le tableau de bord est encore sur `app.py`, le dépôt inclut un `app.py` mince qui charge `main.py`.  
Ne pas commiter `secrets.toml` (déjà ignoré) ; copier les clés dans l’onglet **Secrets** du tableau de bord Streamlit.

```toml
OPENAI_API_KEY = "…"
```

# BioGuide

Application de recherche et d'assistance basée sur des ouvrages historiques de remèdes par les plantes (Gallica).

## Fonctionnalités

- **Les Livres** — Historique des deux ouvrages et de leurs auteurs
- **Recherche IA** — Décrivez vos symptômes, l'assistant cherche dans les ouvrages et synthétise les remèdes
- **À propos** — Mission et méthodologie

## Prérequis

- Python 3.10+
- Clé API OpenAI (pour la synthèse IA)

## Installation sur un nouvel appareil

1. **Cloner le dépôt** (avec [Git LFS](https://git-lfs.com) installé)
   ```bash
   git clone https://github.com/Christophelkhoury/BioGuide_app.git
   cd BioGuide_app
   git lfs pull
   ```
   Sans `git lfs pull`, vous n’avez qu’un pointeur : la base `phyto.db` ne sera pas téléchargée.

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   # source venv/bin/activate   # Linux / macOS
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Base `phyto.db`** (~450 Mo) — fournie via **Git LFS** dans le dépôt.  
   Pour la régénérer depuis zéro (optionnel, long) : `python import_gallica.py`

5. **Configurer la clé OpenAI**
   ```bash
   copy .streamlit\secrets.toml.example .streamlit\secrets.toml   # Windows
   # cp .streamlit/secrets.toml.example .streamlit/secrets.toml     # Linux/Mac
   ```
   Puis éditez `.streamlit/secrets.toml` et remplacez `VOTRE_CLE_ICI` par votre clé.

## Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre dans le navigateur (http://localhost:8501).

## Déploiement Streamlit Cloud

- **Ne commitez jamais** `.streamlit/secrets.toml` (déjà dans `.gitignore`).
- Dans l’admin Streamlit → **Secrets**, ajoutez par exemple :
  ```toml
  OPENAI_API_KEY = "votre-cle"
  ```

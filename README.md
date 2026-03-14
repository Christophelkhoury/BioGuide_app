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

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/Christophelkhoury/BioGuide_app.git
   cd BioGuide_app
   git checkout changes
   ```

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

4. **Créer la base de données** (obligatoire, ~30 min la première fois)
   ```bash
   python import_gallica.py
   ```
   Ce script importe les données depuis Gallica et crée `phyto.db` (~450 Mo).  
   **Note :** Ce fichier n'est pas dans le dépôt (trop volumineux pour GitHub).

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

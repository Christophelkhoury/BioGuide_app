# BioGuide

Application de recherche et d'assistance basée sur des ouvrages historiques de remèdes par les plantes (Gallica).

## Fonctionnalités

- **Sources** — Accès aux deux ouvrages historiques avec citations et liens vers Gallica
- **Recherche** — Recherche TF-IDF dans les passages avec filtres par livre et scores de pertinence
- **Assistant** — Résumé intelligent avec extraits cités (nécessite une clé API OpenAI)

## Prérequis

- Python 3.10+
- Clé API OpenAI (optionnelle, pour l'assistant IA)

## Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
   cd VOTRE_REPO
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

4. **Créer la base de données** (première utilisation uniquement)
   ```bash
   python import_gallica.py
   ```
   Ce script importe les données depuis Gallica et crée `phyto.db`.

5. **Configurer la clé OpenAI** (optionnel, pour l'assistant)
   - Variable d'environnement : `set OPENAI_API_KEY=votre_cle` (Windows) ou `export OPENAI_API_KEY=votre_cle` (Linux/macOS)
   - Ou fichier `.streamlit/secrets.toml` (ne pas committer ce fichier)

## Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre dans le navigateur (par défaut http://localhost:8501).

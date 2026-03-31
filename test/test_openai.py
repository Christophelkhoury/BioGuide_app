#Projet : BioGuide
#Auteurs : Christophe El Khoury, Tia Kahil, Alaa Hamdan
"""Vérifie que la clé API (secrets ou variable d'environnement) permet un appel minimal."""
import os
import sys
from pathlib import Path


def _repo_root() -> Path:
    """Racine du dépôt (parent de ``test/``)."""
    return Path(__file__).resolve().parent.parent


def get_key():
    """Lit OPENAI_API_KEY depuis l'environnement ou .streamlit/secrets.toml."""
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key
    secrets_path = _repo_root() / ".streamlit" / "secrets.toml"
    if os.path.exists(secrets_path):
        with open(secrets_path, encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("#"):
                    continue
                if "OPENAI_API_KEY" in line and "=" in line:
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        key = parts[1].strip()
                        for q in ('"', "'"):
                            if key.startswith(q) and key.endswith(q):
                                key = key[1:-1]
                        key = key.strip()
                        if key and key != "VOTRE_CLE_ICI":
                            return key
    return None

def main():
    """Exécute un appel minimal au service distant pour valider la configuration."""
    key = get_key()
    if not key:
        print("ERREUR: Clé API non trouvée.")
        print("Vérifiez .streamlit/secrets.toml ou la variable OPENAI_API_KEY")
        sys.exit(1)
    if key == "VOTRE_CLE_ICI":
        print("ERREUR: Remplacez VOTRE_CLE_ICI par votre vraie clé dans secrets.toml")
        sys.exit(1)
    print("Clé trouvée (sk-...%s)" % key[-8:])
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Dis 'OK' en un mot."}],
            max_tokens=10,
            timeout=30,
        )
        msg = r.choices[0].message.content if r.choices else ""
        print("Succès! Réponse:", msg)
    except Exception as e:
        print("ERREUR API:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()

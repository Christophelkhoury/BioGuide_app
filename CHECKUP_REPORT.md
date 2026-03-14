# BioGuide — Rapport de vérification (Check-up)

## 1. Base de données phyto.db

### État actuel
- **502 690 passages** indexés
- **Plantes** : 236 469 passages (800 pages)
- **Pauvres** : 266 221 passages (800 pages)
- **Index** : `(book_id, page)` — adapté pour filtrer par livre

### Problème identifié et corrigé
- **FTS5** : La table `passages_fts` n'existait pas (base créée avant l’ajout de FTS).  
  → **Correction** : `init_fts()` a été exécuté. La recherche utilise maintenant FTS5 en priorité, ce qui accélère les requêtes.

### Structure optimale pour les deux livres
La structure actuelle est adaptée :
- Une table `passages` avec `book_id` permet de filtrer par livre
- L’index `idx_passages_book_page` optimise les requêtes par livre
- FTS5 indexe le texte pour la recherche plein texte
- TF-IDF sert de complément pour le classement sémantique

**Recommandation** : Pour une base existante sans FTS, exécuter :
```bash
python -c "from src.db import init_fts; init_fts()"
```

---

## 2. Outil Recherche (pages/2_Recherche.py)

### Points positifs
- Cache du moteur de recherche (`@st.cache_resource`)
- Chaîne de recherche : FTS5 → TF-IDF → fallback SQL
- Normalisation des accents (ex. « fievre » → « fièvre »)
- Bonus thérapeutique pour les passages contenant des termes de remèdes
- Équilibrage des résultats entre les deux livres (round-robin)
- Gestion des erreurs et message si la base est vide

### Problèmes mineurs
- **Cache** : `st.cache_resource.clear()` n’existe pas en Streamlit ; la référence à `st.session_state` pour vider le cache est incorrecte. En cas d’erreur, un simple rerun suffit.

---

## 3. Outil Assistant (pages/3_Assistant.py)

### Problème corrigé
- **LLM non utilisé** : Le module `assistant_llm.py` (reformulation IA) n’était pas appelé.
- **Correction** : Intégration de `reformulate_answer` et `is_llm_available`, avec une case à cocher pour activer la reformulation IA quand `OPENAI_API_KEY` est configurée.

### Autres points
- Vérifications de sécurité (red flags, risk keywords) en place
- Résumé simple par défaut si le LLM n’est pas disponible

---

## 4. Module Safety (src/safety.py)

### Corrections appliquées
- **Doublon** : « enceinte » supprimé dans `RISK_KEYWORDS`.

### Points d’attention (non modifiés)
- **« traitement »** dans `RISK_KEYWORDS` : peut déclencher des faux positifs pour des requêtes comme « traitement naturel ». À envisager : retrait ou remplacement par des termes plus précis (« posologie », « dosage »).
- **« respiration »**, **« crise »** dans `RED_FLAG_KEYWORDS` : termes très généraux (« crise de foie », « respiration » dans un contexte non urgent). À discuter selon le niveau de prudence souhaité.

---

## 5. Import Gallica (import_gallica.py)

### Points positifs
- Appel à `init_db()` et `init_fts()` au démarrage
- Nettoyage OCR via `clean_ocr_text`
- Segmentation en passages (~180 caractères min)
- Seuil de 300 caractères pour ignorer les pages trop courtes

### Points d’attention
- **alto_parser.py** : Non utilisé ; l’import utilise `html_to_text` (lxml) sur le HTML texteImage. Si Gallica change de format, il faudra peut‑être passer à ALTO.
- **Connexion DB** : `import_gallica` ouvre une connexion SQLite directe (`sqlite3.connect`) au lieu d’utiliser `src.db.connect`. Pas bloquant, mais moins cohérent.

---

## 6. Fichiers inutilisés ou vides
- **src/index.py** : Fichier vide
- **src/alto_parser.py** : Présent mais non utilisé (prévu pour un format ALTO)

---

## 7. Performance

- **Mémoire** : Avec ~500k passages, la construction de l’index TF-IDF charge tout en mémoire (plusieurs centaines de Mo). Acceptable pour un usage local.
- **Première recherche** : Construction de l’index TF-IDF + FTS au premier appel. Les suivants sont mis en cache.
- **FTS5** : Réduit fortement le coût de la phase de candidats pour la recherche.

---

## Résumé des corrections appliquées

1. **FTS5** : Initialisation sur `phyto.db` pour activer la recherche plein texte.
2. **Assistant** : Intégration du LLM (`reformulate_answer`) avec option d’activation.
3. **Safety** : Suppression du doublon « enceinte » dans `RISK_KEYWORDS`.

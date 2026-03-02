"""
BioGuide - About / Method page
"""
import streamlit as st
from src.ui_components import render_disclaimer, load_global_css

st.set_page_config(
    page_title="BioGuide — À propos",
    layout="wide",
)

# Load global responsive CSS
load_global_css()

# Sidebar
with st.sidebar:
    st.markdown("# BioGuide")
    st.markdown("---")
    st.markdown("### Navigation")
    if st.button("Accueil"):
        st.switch_page("app.py")
    if st.button("Sources / livres"):
        st.switch_page("pages/1_Livres.py")
    if st.button("Recherche"):
        st.switch_page("pages/2_Recherche.py")
    if st.button("Assistant"):
        st.switch_page("pages/3_Assistant.py")

st.title("À propos")

st.markdown(
    """
    Cette page décrit la méthodologie technique, les limitations, et les considérations éthiques de l'application BioGuide.
    """
)

# Pipeline section
st.markdown("---")
st.markdown("### Pipeline technique")

st.markdown(
    """
    #### 1. Collecte des données (Gallica texteImage)
    
    - Extraction du texte OCR depuis les pages numérisées de Gallica
    - Utilisation de l'API texteImage pour chaque page
    - Nettoyage basique du texte OCR (normalisation des espaces, suppression des caractères spéciaux)
    
    #### 2. Nettoyage et segmentation
    
    - **Nettoyage** : Suppression des caractères de césure, normalisation des espaces
    - **Segmentation** : Découpage du texte en passages de ~180 caractères minimum
    - Stockage dans une base SQLite avec métadonnées (book_id, page)
    
    #### 3. Indexation TF-IDF
    
    - Utilisation de scikit-learn `TfidfVectorizer`
    - Paramètres :
      - N-grammes : 1-2 (mots et bigrammes)
      - Max features : 5000
      - Min document frequency : 2
      - Max document frequency : 95%
    - Calcul de similarité cosinus pour la recherche
    
    #### 4. Interface Streamlit
    
    - **Page Recherche** : Recherche TF-IDF avec filtres et scores
    - **Page Assistant** : Récupération des top-k passages + résumé structuré
    - **Sécurité** : Détection de symptômes critiques et avertissements médicaux
    """
)

# Safety & Ethics
st.markdown("---")
st.markdown("### Sécurité et éthique")

st.markdown(
    """
    #### Avertissements médicaux
    
    - **Déni de responsabilité** : Les informations proviennent de sources historiques et ne constituent 
      pas un avis médical professionnel.
    - **Détection de symptômes critiques** : L'application détecte les recherches contenant des symptômes 
      d'urgence (douleur thoracique, difficulté respiratoire, etc.) et affiche un avertissement proéminent.
    - **Avis de risque** : Pour les sujets sensibles (grossesse, allergies, médicaments), un avis de 
      précaution est affiché.
    
    #### Considérations éthiques
    
    - **Sources historiques** : Les remèdes proposés peuvent être obsolètes ou dangereux selon les 
      connaissances médicales actuelles.
    - **Pas de diagnostic** : L'application ne fournit jamais de diagnostic médical.
    - **Orientation vers les professionnels** : Toujours consulter un professionnel de santé qualifié.
    - **Transparence** : Toutes les citations sont visibles et vérifiables sur Gallica.
    """
)

# Limitations
st.markdown("---")
st.markdown("### Limitations")

st.markdown(
    """
    #### Techniques
    
    - **Qualité OCR** : Les erreurs d'OCR peuvent affecter la recherche et les résultats.
    - **TF-IDF simple** : Pas de compréhension sémantique avancée (pas de LLM pour la génération de résumés).
    - **Langue historique** : Le français des ouvrages peut différer du français moderne.
    - **Segmentation** : Les passages peuvent être coupés au milieu d'une phrase.
    
    #### Contenu
    
    - **Médecine historique** : Les remèdes peuvent être inefficaces ou dangereux selon les standards modernes.
    - **Contexte manquant** : Certaines informations de contexte peuvent être perdues lors de la segmentation.
    - **Pas de validation médicale** : Aucune validation par des professionnels de santé.
    
    #### Performance
    
    - **Temps de réponse** : La construction de l'index TF-IDF peut prendre quelques secondes au premier chargement.
    - **Base de données** : SQLite peut devenir lent avec de très grandes quantités de données.
    """
)

# Future work
st.markdown("---")
st.markdown("### Travaux futurs")

st.markdown(
    """
    - **Amélioration de la recherche** : Intégration d'embeddings sémantiques (sentence transformers)
    - **Résumés intelligents** : Utilisation d'un LLM pour générer des résumés plus cohérents
    - **Interface améliorée** : Historique de recherche, favoris, export de citations
    - **Plus d'ouvrages** : Extension à d'autres livres de Gallica
    - **Validation médicale** : Collaboration avec des professionnels pour annoter les remèdes
    - **Multilingue** : Support d'autres langues et ouvrages
    """
)

# Credits
st.markdown("---")
st.markdown("### Crédits")

# Responsive credits columns
col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

with col1:
    st.markdown(
        """
        **Membre 1**  
        Responsabilité : [À compléter]
        """
    )

with col2:
    st.markdown(
        """
        **Membre 2**  
        Responsabilité : [À compléter]
        """
    )

with col3:
    st.markdown(
        """
        **Membre 3**  
        Responsabilité : [À compléter]
        """
    )

st.markdown(
    """
    **Remerciements :**
    - Bibliothèque nationale de France (BnF) pour l'accès à Gallica
    - Projet Gallica pour la numérisation et l'OCR des ouvrages
    """
)

# Technical stack
st.markdown("---")
st.markdown("### Stack technique")

st.markdown(
    """
    - **Frontend** : Streamlit
    - **Backend** : Python 3.x
    - **Base de données** : SQLite
    - **Recherche** : scikit-learn (TF-IDF)
    - **Traitement texte** : regex, lxml
    - **Déploiement** : [À compléter]
    """
)

# Disclaimer
render_disclaimer()

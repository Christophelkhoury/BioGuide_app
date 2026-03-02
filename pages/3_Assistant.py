"""
BioGuide - Assistant page
"""
import streamlit as st
from src.search import SearchEngine
from src.safety import (
    check_red_flags,
    check_risk_keywords,
    get_red_flag_message,
    get_risk_notice,
)
from src.ui_components import render_citation, render_disclaimer, render_warning, BOOK_INFO, load_global_css, clean_text_for_display

# Cache search engine initialization
@st.cache_resource
def get_cached_search_engine(book_filter):
    """Get cached search engine instance."""
    engine = SearchEngine()
    engine.build_index(book_filter)
    return engine

st.set_page_config(
    page_title="BioGuide — Assistant",
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
    if st.button("À propos"):
        st.switch_page("pages/4_A_propos.py")
    
    st.markdown("---")
    st.markdown("### Paramètres")
    
    # Book filter
    book_options = ["Tous"] + [info["short_title"] for info in BOOK_INFO.values()]
    selected_book_display = st.selectbox("Filtrer par livre", book_options)
    
    book_filter = None
    if selected_book_display != "Tous":
        for book_id, info in BOOK_INFO.items():
            if info["short_title"] == selected_book_display:
                book_filter = book_id
                break
    
    # Top-k slider
    top_k = st.slider("Nombre d'extraits", min_value=3, max_value=10, value=5, step=1)

st.title("Assistant")

st.markdown(
    """
    Posez une question et obtenez un résumé avec des extraits cités des ouvrages historiques. 
    L'assistant utilise la recherche TF-IDF pour trouver les passages les plus pertinents.
    """
)

# Initialize session state for conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input - responsive
query = st.text_area(
    "Votre question",
    placeholder="Ex: Comment soigner un mal de tête ? Quels remèdes pour la fièvre ?",
    height=100,
    label_visibility="collapsed",
)

# Submit button - responsive
col1, col2 = st.columns([1, 5], gap="small")
with col1:
    submit_button = st.button("Envoyer", type="primary", use_container_width=True)

# Process query
if submit_button and query.strip():
    # Safety checks
    has_red_flags, red_flag_keywords = check_red_flags(query)
    has_risks, risk_keywords = check_risk_keywords(query)
    
    # Show red flag warning and stop
    if has_red_flags:
        render_warning(get_red_flag_message(red_flag_keywords), level="danger")
        st.markdown(
            """
            **Cette application ne peut pas fournir de diagnostic médical.**
            
            Pour des symptômes graves ou urgents, consultez immédiatement :
            - **15** (SAMU) pour les urgences médicales
            - **112** (numéro d'urgence européen)
            - Votre médecin traitant
            """
        )
        render_disclaimer()
        st.stop()
    
    # Show risk notice
    if has_risks:
        render_warning(get_risk_notice(risk_keywords), level="info")
    
    # Perform search and generate summary
    with st.spinner("Recherche et analyse en cours..."):
        try:
            # Initialize search engine (cached)
            engine = get_cached_search_engine(book_filter)
            results = engine.search(query, top_k=top_k)
            
            if results:
                # Display summary section
                st.markdown("---")
                st.markdown("### Résumé")
                
                # Generate simple summary (3 bullet points)
                summary_points = []
                for i, (book_id, page, text, score) in enumerate(results[:3], 1):
                    # Clean text before processing
                    cleaned_text = clean_text_for_display(text)
                    # Extract first sentence or first 150 chars
                    first_sentence = cleaned_text.split(".")[0] if "." in cleaned_text else cleaned_text[:150]
                    summary_points.append(f"{i}. {first_sentence}...")
                
                for point in summary_points:
                    st.markdown(f"- {point}")
                
                # Display cited extracts
                st.markdown("---")
                st.markdown("### Extraits cités")
                
                for idx, (book_id, page, text, score) in enumerate(results, 1):
                    citation_html = render_citation(book_id, page)
                    cleaned_text = clean_text_for_display(text)
                    
                    with st.expander(f"Extrait {idx}", expanded=(idx <= 2)):
                        st.markdown(f"**Citation:** {citation_html}", unsafe_allow_html=True)
                        st.markdown("---")
                        st.markdown(f"**Texte:**")
                        st.markdown(f"> {cleaned_text}")
                        
                        # Copy button
                        if st.button(f"📋 Copier l'extrait {idx}", key=f"copy_extract_{idx}"):
                            st.code(cleaned_text, language=None)
                            st.success("Extrait copié!")
            else:
                st.info("Aucun résultat trouvé pour votre question.")
                st.markdown(
                    """
                    **Suggestions :**
                    - Reformulez votre question
                    - Utilisez des termes plus généraux
                    - Vérifiez le filtre de livre sélectionné
                    """
                )
        
        except Exception as e:
            st.error(f"Erreur lors du traitement: {e}")
            st.exception(e)

elif submit_button and not query.strip():
    st.warning("Veuillez entrer une question.")

else:
    # Instructions
    st.info("Entrez votre question ci-dessus pour obtenir un résumé avec des extraits cités.")
    st.markdown(
        """
        **Exemples de questions :**
        - Comment soigner un mal de tête ?
        - Quels remèdes pour la fièvre ?
        - Traitement naturel contre la toux
        - Plantes médicinales pour les douleurs
        """
    )

# Disclaimer
st.markdown("---")
render_disclaimer()

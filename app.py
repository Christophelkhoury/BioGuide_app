"""
BioGuide - Main Streamlit app (Home page)
"""
import streamlit as st
from src.db import connect
from src.ui_components import render_disclaimer, load_global_css

# Cache database queries
@st.cache_data
def get_db_stats():
    """Get cached database statistics."""
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM passages")
    num_passages = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(DISTINCT book_id || '-' || page) FROM passages")
    num_pages = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM books")
    num_books = cur.fetchone()[0]
    
    conn.close()
    return num_passages, num_pages, num_books

# Page configuration
st.set_page_config(
    page_title="BioGuide — Accueil",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load global responsive CSS
load_global_css()

# Sidebar navigation
with st.sidebar:
    st.markdown("# BioGuide")
    st.markdown("---")
    
    st.markdown("### Navigation")
    page = st.radio(
        "Choisir une page",
        ["Accueil", "Livres", "Recherche", "Assistant", "À propos"],
        label_visibility="collapsed",
    )
    
    # Note: Streamlit automatically handles page navigation via the pages/ directory
    # The radio is for display only - actual navigation happens via URL
    
    st.markdown("---")
    st.markdown("### À propos")
    st.markdown(
        "Application de recherche et d'assistance basée sur des ouvrages historiques "
        "de remèdes par les plantes de Gallica."
    )

# Hero section
st.markdown(
    """
    <div class="hero">
        <h1>BioGuide</h1>
        <p>Remèdes par les plantes (Gallica)</p>
        <p style="font-size: 1rem; color: #6B7280;">
            Recherche et assistance basées sur deux ouvrages historiques de référence.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Feature cards - responsive columns
st.markdown("### Fonctionnalités")
# Use responsive columns that stack on mobile
col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <h3>Sources</h3>
            <p>Accédez aux deux ouvrages historiques avec leurs citations complètes et liens vers Gallica.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <h3>Recherche</h3>
            <p>Recherche TF-IDF avancée dans les passages avec filtres par livre et scores de pertinence.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <h3>Assistant</h3>
            <p>Résumé intelligent avec extraits cités et couche de sécurité pour les symptômes critiques.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Quick stats
st.markdown("---")
st.markdown("### Statistiques")

try:
    num_passages, num_pages, num_books = get_db_stats()
    
    # Responsive stats columns
    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
    
    with col1:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-number">{num_passages:,}</div>
                <div class="stat-label">Passages indexés</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-number">{num_pages:,}</div>
                <div class="stat-label">Pages indexées</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-number">{num_books}</div>
                <div class="stat-label">Ouvrages disponibles</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

except Exception as e:
    st.error(f"Erreur lors du chargement des statistiques: {e}")

# CTA buttons - responsive
st.markdown("---")
st.markdown("### Démarrer")
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    if st.button("Aller à la recherche", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Recherche.py")

with col2:
    if st.button("Ouvrir l'assistant", use_container_width=True, type="secondary"):
        st.switch_page("pages/3_Assistant.py")

# Disclaimer
render_disclaimer()

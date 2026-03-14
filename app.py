"""
BioGuide - Accueil
"""
import streamlit as st
from src.db import connect
from src.ui_components import render_disclaimer, load_global_css, render_top_nav

@st.cache_data
def get_db_stats():
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

st.set_page_config(page_title="BioGuide", layout="wide", initial_sidebar_state="collapsed")

load_global_css()
render_top_nav("")

# Hero
st.markdown(
    """
    <div class="hero-section">
        <h1 class="hero-title">BioGuide</h1>
        <p class="hero-sub">Remèdes par les plantes</p>
        <p class="hero-sub" style="font-size: 0.95rem; opacity: 0.85;">Deux ouvrages historiques de Gallica</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Summary cards
try:
    num_passages, num_pages, num_books = get_db_stats()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="stat-card"><div class="stat-value">{num_passages:,}</div><div class="stat-label">Passages indexés</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="stat-card"><div class="stat-value">{num_pages:,}</div><div class="stat-label">Pages</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="stat-card"><div class="stat-value">{num_books}</div><div class="stat-label">Ouvrages</div></div>',
            unsafe_allow_html=True,
        )
except Exception:
    pass

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

st.markdown("**Commencer**")
if st.button("Recherche avec IA", type="primary", use_container_width=True):
    st.switch_page("pages/2_Recherche_avec_IA.py")

render_disclaimer()

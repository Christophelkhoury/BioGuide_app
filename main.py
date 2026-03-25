"""Point d'entrée Streamlit — page d'accueil BioGuide."""
import streamlit as st
from src.db import connect
from src.ui_components import render_disclaimer, load_global_css, render_top_nav


@st.cache_data
def get_db_stats():
    """Retourne le nombre de passages, de pages distinctes et d'ouvrages en base."""
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

st.markdown(
    """
    <div class="hero-section">
        <h1 class="hero-title">BioGuide</h1>
        <p class="hero-sub">Remèdes par les plantes</p>
        <p class="hero-sub" style="font-size: 0.95rem;">Deux ouvrages historiques de Gallica</p>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    num_passages, num_pages, num_books = get_db_stats()
    st.markdown(
        f"""
        <div class="section-livres">
            <h3 style="color:#3d4f42;margin:0 0 4px 0;font-size:1.25rem;">Les livres</h3>
            <p style="color:#5a6f5c;font-size:0.9rem;margin:0 0 20px 0;">Aperçu du contenu indexé dans l'application.</p>
            <div style="display:flex;flex-wrap:wrap;gap:16px;justify-content:center;">
                <div class="stat-card" style="flex:1;min-width:140px;max-width:280px;">
                    <div class="stat-value">{num_passages:,}</div><div class="stat-label">Passages indexés</div>
                </div>
                <div class="stat-card" style="flex:1;min-width:140px;max-width:280px;">
                    <div class="stat-value">{num_pages:,}</div><div class="stat-label">Pages</div>
                </div>
                <div class="stat-card" style="flex:1;min-width:140px;max-width:280px;">
                    <div class="stat-value">{num_books}</div><div class="stat-label">Ouvrages</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
except Exception:
    pass

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

st.markdown("**Commencer**")
if st.button("Recherche IA", type="primary", use_container_width=True):
    st.switch_page("pages/2_Recherche_avec_IA.py")

render_disclaimer()

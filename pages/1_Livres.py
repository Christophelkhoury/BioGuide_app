"""
BioGuide - Les Livres
Design rustique, historique des deux ouvrages et de leurs auteurs.
"""
import streamlit as st
from src.ui_components import (
    BOOK_INFO,
    render_disclaimer,
    load_global_css,
    render_top_nav,
)

st.set_page_config(page_title="BioGuide — Les Livres", layout="wide", initial_sidebar_state="collapsed")

load_global_css(theme="rustic")
render_top_nav("pages/1_Livres.py")

# Bandeau rustique (vert doux + bordure)
st.markdown(
    """
    <div class="rustic-banner" style="text-align: center;">
        <div class="rustic-banner-title">Les Livres</div>
        <p class="rustic-banner-sub" style="margin: 0;">Deux trésors de la médecine populaire du XIXe siècle</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# Carte livre 1 - Jules Clément
with st.container():
    info = BOOK_INFO["plantes"]
    st.markdown(
        f"""
        <div class="rustic-card">
            <h2 class="rustic-title">{info['title']}</h2>
            <p style="color: #6b5b45; font-style: italic; margin: 8px 0;">Par {info['author']} — {info['year']}</p>
            <p style="margin: 16px 0; line-height: 1.6;">
                Jules Clément publie ce traité de médecine populaire dans les années 1860, à une époque où 
                les remèdes chimiques commencent à envahir les pharmacies. Son ouvrage propose un retour 
                aux <strong>propriétés des plantes</strong> : des traitements simples, peu coûteux et accessibles 
                à tous. L'hygiène populaire et un dictionnaire des termes médicaux complètent ce guide 
                précieux pour les familles modestes.
            </p>
            <p style="margin: 16px 0; line-height: 1.6;">
                Ce livre a connu plusieurs éditions et reste une référence pour qui souhaite redécouvrir 
                les savoirs des herboristes d'autrefois.
            </p>
            <p style="margin-top: 20px;">
                <a href="{info['source_url']}" target="_blank" rel="noopener">→ Consulter sur Gallica</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Carte livre 2 - Dr Beauvillard
with st.container():
    info = BOOK_INFO["pauvres"]
    st.markdown(
        f"""
        <div class="rustic-card">
            <h2 class="rustic-title">{info['title']}</h2>
            <p style="color: #6b5b45; font-style: italic; margin: 8px 0;">Par {info['author']} — {info['year']} (39e édition)</p>
            <p style="margin: 16px 0; line-height: 1.6;">
                Le Dr Beauvillard, médecin humaniste et Chevalier de la Légion d'honneur, consacre sa vie 
                à la santé des classes populaires. <strong>Le Médecin des pauvres</strong> connaît un succès 
                exceptionnel : la 39e édition témoigne de l'engouement pour ces remèdes naturels et 
                accessibles.
            </p>
            <p style="margin: 16px 0; line-height: 1.6;">
                Son approche privilégie les plantes, les préparations maison et les conseils d'hygiène 
                plutôt que les médicaments coûteux. Un héritage précieux que BioGuide met à portée 
                de clic grâce à l'intelligence artificielle.
            </p>
            <p style="margin-top: 20px;">
                <a href="{info['source_url']}" target="_blank" rel="noopener">→ Consulter sur Gallica</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# CTA vers la recherche IA
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="rustic-banner" style="text-align: center;">
        <p class="rustic-banner-sub" style="margin: 0;">
            Prêt à explorer ces savoirs ? Utilisez la <strong>Recherche IA</strong> pour trouver des remèdes adaptés à vos symptômes.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("Aller à la Recherche IA", type="primary", use_container_width=True):
    st.switch_page("pages/2_Recherche_avec_IA.py")

render_disclaimer()

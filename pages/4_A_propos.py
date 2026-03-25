"""Page « À propos » : mission et méthodologie de BioGuide."""
import streamlit as st
from src.ui_components import render_disclaimer, load_global_css, render_top_nav, APP_SLOGAN

st.set_page_config(
    page_title="BioGuide — À propos",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_global_css()
render_top_nav("pages/4_A_propos.py")

st.markdown("")
st.markdown(
    f"""
    <div class="bg-card" style="text-align: center; padding: 28px 24px; margin-bottom: 28px;">
        <p class="slogan-accent" style="font-size: 1.45rem; font-weight: 700; margin: 0; letter-spacing: -0.02em;">
            {APP_SLOGAN}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")
st.markdown(
    """
    <div class="bg-card">
        <h2 style="margin: 0 0 12px 0;">Notre mission</h2>
        <p style="margin: 0 0 12px 0; line-height: 1.6;">
            <strong>BioGuide</strong> a pour but d'<strong>emprunter les anciens remèdes naturels</strong> à la place des médicaments
            nocifs d'aujourd'hui. Face à une pharmacopée chimique parfois agressive, nous proposons de
            redécouvrir le savoir des herboristes et des médecins populaires du XIXe siècle.
        </p>
        <ul style="margin: 0; padding-left: 1.25rem; line-height: 1.7;">
            <li><strong>Deux ouvrages historiques</strong> numérisés par la BnF (Gallica) : <em>La santé par les plantes</em>
                de Jules Clément et <em>Le médecin des pauvres</em> du Dr Beauvillard.</li>
            <li><strong>Une recherche assistée par l'IA</strong> : décrivez vos symptômes, l'assistant parcourt les
                textes et synthétise les remèdes proposés avec leurs sources.</li>
            <li><strong>Des liens directs</strong> vers les pages Gallica pour consulter les ouvrages originaux.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")
st.markdown(
    """
    <div class="bg-card">
        <h2 style="margin: 0 0 12px 0;">Comment ça marche ?</h2>
        <p style="margin: 0; line-height: 1.6;">
            La recherche utilise <strong>TF-IDF</strong> pour retrouver les passages pertinents dans les deux livres,
            puis un <strong>assistant IA</strong> (OpenAI) pour synthétiser les résultats et les présenter de façon
            claire. Les informations restent historiques : consultez toujours un professionnel de santé
            avant d'utiliser un remède.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")
st.markdown("## Avertissement")

render_disclaimer()

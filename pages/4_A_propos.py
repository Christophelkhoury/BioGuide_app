"""
BioGuide - À propos
But de l'app : emprunter les anciens remèdes naturels à la place des médicaments nocifs.
"""
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
# Slogan principal
st.markdown(
    f"""
    <div style="text-align: center; padding: 32px 24px; background: linear-gradient(135deg, rgba(59,164,247,0.1) 0%, rgba(41,199,172,0.1) 100%); border-radius: 16px; margin-bottom: 32px; border: 1px solid rgba(59,164,247,0.2);">
        <p style="font-size: 1.5rem; font-weight: 700; color: #1F2A37; margin: 0; letter-spacing: -0.02em;">
            {APP_SLOGAN}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")
st.markdown("## Notre mission")

st.markdown(
    """
    **BioGuide** a pour but d'**emprunter les anciens remèdes naturels** à la place des médicaments 
    nocifs d'aujourd'hui. Face à une pharmacopée chimique parfois agressive, nous proposons de 
    redécouvrir le savoir des herboristes et des médecins populaires du XIXe siècle.

    - **Deux ouvrages historiques** numérisés par la BnF (Gallica) : *La santé par les plantes* 
      de Jules Clément et *Le médecin des pauvres* du Dr Beauvillard.
    - **Une recherche assistée par l'IA** : décrivez vos symptômes, l'assistant parcourt les 
      textes et synthétise les remèdes proposés avec leurs sources.
    - **Des liens directs** vers les pages Gallica pour consulter les ouvrages originaux.
    """
)

st.markdown("")
st.markdown("## Comment ça marche ?")

st.markdown(
    """
    La recherche utilise **TF-IDF** pour retrouver les passages pertinents dans les deux livres, 
    puis un **assistant IA** (OpenAI) pour synthétiser les résultats et les présenter de façon 
    claire. Les informations restent historiques : consultez toujours un professionnel de santé 
    avant d'utiliser un remède.
    """
)

st.markdown("")
st.markdown("## Avertissement")

render_disclaimer()

"""Composants d'interface et styles globaux Streamlit."""
import base64
import re
from pathlib import Path
from typing import Optional

import streamlit as st

COLORS = {
    "primary": "#3d4f42",
    "secondary": "#5f8f7a",
    "bg_main": "#e8f2ea",
    "bg_secondary": "#f5f0e6",
    "bg_card": "#f5f0e6",
    "text_main": "#2d3d2f",
    "text_secondary": "#5a6f5c",
    "text_muted": "#6b7d6e",
    "success": "#22C55E",
    "warning": "#c4a574",
    "error": "#b4534a",
}

BOOK_INFO = {
    "plantes": {
        "title": "La santé ou la médecine populaire",
        "short_title": "Plantes",
        "author": "Jules Clément",
        "year": "1860-1869",
        "ark": "bpt6k5688257m",
        "source_url": "https://gallica.bnf.fr/ark:/12148/bpt6k5688257m",
        "color": COLORS["secondary"],
    },
    "pauvres": {
        "title": "Le médecin des pauvres",
        "short_title": "Pauvres",
        "author": "Dr Beauvillard",
        "year": "XIXe-XXe siècle",
        "ark": "bpt6k5791358q",
        "source_url": "https://gallica.bnf.fr/ark:/12148/bpt6k5791358q",
        "color": COLORS["primary"],
    },
}

APP_SLOGAN = "Des remèdes d'hier, une santé sans chimie."


def get_gallica_page_url(book_id: str, page: int) -> str:
    """Retourne l'URL Gallica pour une page donnée d'un ouvrage."""
    ark = BOOK_INFO.get(book_id, {}).get("ark", "")
    return f"https://gallica.bnf.fr/ark:/12148/{ark}/f{page}"


def _get_dark_mode() -> bool:
    """Indique si le mode sombre est actif dans la session."""
    return st.session_state.get("dark_mode", False) if "dark_mode" in st.session_state else False


def _parchment_bg_url() -> Optional[str]:
    """Charge le fond parchemin optionnel en data URL pour le CSS."""
    base = Path(__file__).resolve().parent.parent / "assets"
    for name, mime in (("bioguide-bg.png", "image/png"), ("bioguide-bg.jpg", "image/jpeg"), ("bioguide-bg.jpeg", "image/jpeg")):
        path = base / name
        if path.is_file():
            try:
                raw = path.read_bytes()
                b64 = base64.b64encode(raw).decode("ascii")
                return f"url(data:{mime};base64,{b64})"
            except OSError:
                return None
    return None


def _logo_data_url() -> Optional[str]:
    """Charge le logo en data URL pour l'en-tête."""
    path = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
    if not path.is_file():
        return None
    try:
        raw = path.read_bytes()
        b64 = base64.b64encode(raw).decode("ascii")
        return f"data:image/png;base64,{b64}"
    except OSError:
        return None


def load_global_css(dark_mode: Optional[bool] = None, theme: str = "default"):
    """Injecte les styles CSS (thèmes default, rustic, hybrid)."""
    if dark_mode is None:
        dark_mode = _get_dark_mode()

    hide_css = """
    footer { visibility: hidden; }
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    """

    bg_url = _parchment_bg_url()
    leaf_pattern = (
        "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80'%3E"
        "%3Cpath fill='%233d4f42' fill-opacity='0.06' d='M5 75 Q25 35 45 55 Q35 25 70 15 Q50 40 55 75 Z'/%3E"
        "%3Ccircle cx='65' cy='65' r='3' fill='%23c4b5a0' fill-opacity='0.35'/%3E"
        "%3C/svg%3E\")"
    )

    if bg_url:
        if theme == "rustic":
            app_bg = f"""
        .stApp, [data-testid="stAppViewContainer"] {{
            background-color: #e8f2ea !important;
            background-image: linear-gradient(rgba(232,242,234,0.78), rgba(232,242,234,0.88)), {bg_url} !important;
            background-size: auto, cover !important;
            background-position: center, center !important;
            background-attachment: fixed !important;
        }}"""
        elif theme == "hybrid":
            app_bg = f"""
        .stApp, [data-testid="stAppViewContainer"] {{
            background-color: #e8f2ea !important;
            background-image: linear-gradient(135deg, rgba(232,242,234,0.75) 0%, rgba(220,235,245,0.82) 55%, rgba(232,242,234,0.88) 100%), {bg_url} !important;
            background-size: auto, cover !important;
            background-position: center, center !important;
            background-attachment: fixed !important;
        }}"""
        else:
            app_bg = f"""
        .stApp, [data-testid="stAppViewContainer"] {{
            background-color: #e8f2ea !important;
            background-image: linear-gradient(rgba(232,242,234,0.82), rgba(232,242,234,0.9)), {bg_url} !important;
            background-size: auto, cover !important;
            background-position: center, center !important;
            background-attachment: fixed !important;
        }}"""
    else:
        app_bg = """
        .stApp, [data-testid="stAppViewContainer"] {
            background-color: #e8f2ea !important;
            background-image: linear-gradient(180deg, rgba(232,242,234,0.97) 0%, rgba(220,232,224,0.98) 100%),
                radial-gradient(ellipse 70% 45% at 100% 0%, rgba(196,181,160,0.22), transparent 60%),
                radial-gradient(ellipse 50% 40% at 0% 100%, rgba(95,143,122,0.12), transparent 55%) !important;
            background-attachment: fixed !important;
        }"""

    page_theme = ""
    if theme == "rustic":
        page_theme = """
        .main .block-container { background: transparent !important; }
        .rustic-banner { background: linear-gradient(180deg, #dce8df 0%, #c8d9cc 100%) !important;
            border: 2px solid #3d4f42 !important; border-radius: 16px !important; padding: 20px 24px !important;
            margin: 24px 0 !important; box-shadow: 0 4px 20px rgba(61,79,66,0.12) !important; }
        .rustic-banner .rustic-banner-title { color: #3d4f42 !important; font-size: 1.45rem !important; font-weight: 700 !important; }
        .rustic-banner .rustic-banner-sub { color: #5a6f5c !important; font-size: 0.95rem !important; margin-top: 8px !important; }
        .rustic-card, .bg-card { background: #f5f0e6 !important; border: 2px solid #3d4f42 !important; border-radius: 16px !important;
            padding: 28px !important; margin: 24px 0 !important; color: #2d3d2f !important;
            box-shadow: 0 2px 12px rgba(45,61,47,0.08) !important; }
        .rustic-title, .bg-card h2 { color: #3d4f42 !important; font-size: 1.35rem !important; font-weight: 700 !important; }
        .rustic-curtain { display: none !important; }
        a { color: #3d4f42 !important; font-weight: 600 !important; }
        """
    elif theme == "hybrid":
        page_theme = """
        .main .block-container { background: transparent !important; padding-bottom: 140px !important; }
        .hybrid-intro { background: #f5f0e6 !important; border: 2px solid #3d4f42 !important; border-radius: 16px !important;
            padding: 20px 24px !important; margin: 16px 0 24px 0 !important; color: #2d3d2f !important; }
        .hybrid-intro h2, .hybrid-intro h3 { color: #3d4f42 !important; font-weight: 700 !important; }
        .hybrid-glass { background: rgba(255,255,255,0.55) !important; border: 1px solid rgba(61,79,66,0.2) !important;
            border-radius: 14px !important; backdrop-filter: blur(8px) !important; }
        .main .block-container p, .main .block-container span, .main .block-container div,
        .main .block-container label, [data-testid="stMarkdown"] p, [data-testid="stMarkdown"] span,
        [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span { color: #2d3d2f !important; }
        [data-testid="stChatInput"] {
            position: fixed !important; bottom: 0 !important; left: 50% !important;
            transform: translateX(-50%) !important; width: 100% !important; max-width: 640px !important;
            padding: 16px 24px 24px !important;
            background: linear-gradient(180deg, transparent 0%, rgba(232,242,234,0.97) 25%, #e8f2ea 100%) !important;
            z-index: 999 !important;
        }
        [data-testid="stChatInput"] textarea {
            min-height: 52px !important; max-height: 120px !important;
            border-radius: 20px !important; border: 2px solid #3d4f42 !important;
            background: #f5f0e6 !important; color: #2d3d2f !important;
            padding: 14px 20px !important; font-size: 1rem !important;
            box-shadow: 0 2px 16px rgba(61,79,66,0.12) !important;
        }
        """

    if dark_mode:
        theme_css = """
        .stApp { background: #1a2420 !important; }
        [data-testid="stAppViewContainer"] { background: #1a2420 !important; }
        .main .block-container { background: transparent !important; }
        .main .block-container p, .main .block-container span, .main .block-container div,
        .main .block-container label, [data-testid="stMarkdown"] p, [data-testid="stMarkdown"] span,
        [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span { color: #dce8df !important; }
        .hero-title, .brand-title { color: #b8cbb8 !important; }
        .hero-sub, .brand-slogan { color: #8fa894 !important; }
        .stat-card { background: #2a3530 !important; border: 2px solid #4a5c52 !important; color: #dce8df !important; }
        .stat-value { color: #c4d4c8 !important; }
        .stat-label { color: #9aaf9f !important; }
        .disclaimer-box { background: #2f2a28 !important; border: 2px solid #c49a9e !important; color: #e8ddd4 !important; }
        .bg-card, .rustic-card { background: #2a3530 !important; border-color: #5f8f7a !important; color: #dce8df !important; }
        .slogan-accent { color: #c4a574 !important; }
        a { color: #8fbc8f !important; }
        .citation-page { color: #9aaf9f !important; }
        """
    else:
        theme_css = f"""
        {app_bg}
        .main .block-container {{
            background: transparent !important;
            background-image: {leaf_pattern} !important;
            background-size: 80px 80px !important;
        }}
        .hero-title, .brand-title {{ color: #3d4f42 !important; }}
        .hero-sub {{ color: #5a6f5c !important; }}
        .brand-slogan {{ color: #5a6f5c !important; }}
        .stat-card {{
            background: #f5f0e6 !important; border: 2px solid #3d4f42 !important; border-radius: 16px !important;
            box-shadow: 0 2px 10px rgba(61,79,66,0.08) !important;
        }}
        .stat-value {{ color: #3d4f42 !important; }}
        .stat-label {{ color: #5a6f5c !important; }}
        .disclaimer-box {{
            background: #f5f0e6 !important; border: 2px solid #d4a5a8 !important; border-radius: 16px !important;
            color: #2d3d2f !important;
        }}
        .section-livres {{
            background: linear-gradient(180deg, #dce8df 0%, #d0e0d4 100%) !important;
            border-radius: 16px !important; padding: 28px 24px !important; margin: 24px 0 !important;
            border: 1px solid rgba(61,79,66,0.2) !important;
        }}
        .slogan-accent {{ color: #7d6f50 !important; }}
        .bg-card {{ background: #f5f0e6 !important; border: 2px solid #3d4f42 !important; border-radius: 16px !important;
            padding: 24px !important; margin: 20px 0 !important; color: #2d3d2f !important; }}
        .bg-card h2, .bg-card h3 {{ color: #3d4f42 !important; font-weight: 700 !important; }}
        a {{ color: #3d4f42 !important; font-weight: 600 !important; }}
        .citation-page {{ color: #5a6f5c !important; }}
        .main h1, .main h2, .main h3, [data-testid="stMarkdown"] h1, [data-testid="stMarkdown"] h2, [data-testid="stMarkdown"] h3 {{
            color: #3d4f42 !important;
        }}
        """

    anim_css = """
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .stat-card { animation: fadeInUp 0.25s ease-out; }
    """

    layout_css = """
        .block-container { padding: 40px 48px 48px; max-width: 960px; }
        .hero-section { text-align: center; padding: 48px 24px 40px; }
        .hero-title { font-size: 2rem; font-weight: 700; margin-bottom: 8px; letter-spacing: -0.02em; }
        .hero-sub { font-size: 1.05rem; margin-bottom: 4px; }
        .stat-card { padding: 24px; text-align: center; margin-bottom: 20px;
                     transition: transform 0.2s ease, box-shadow 0.2s ease; }
        .stat-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(61,79,66,0.14) !important; }
        .stat-value { font-size: 1.75rem; font-weight: 700; margin-bottom: 4px; }
        .stat-label { font-size: 0.9rem; }
        .section-spacer { margin: 40px 0; }
        .brand-logo {
            max-height: 110px;
            width: auto;
            margin: 0 auto 14px auto;
            display: block;
            border-radius: 18px;
            box-shadow: 0 4px 18px rgba(61, 79, 66, 0.18);
            object-fit: contain;
        }
    """

    nav_css = """
        .block-container { padding-top: 32px !important; overflow: visible !important; }
        .block-container > div:first-child { margin-bottom: 20px !important; overflow: visible !important; }
        .block-container > div:nth-child(2) { margin-bottom: 28px !important; overflow: visible !important; }
        .block-container > div:nth-child(2) [data-testid="column"] { padding: 0 10px !important; overflow: visible !important; }
        .block-container > div:nth-child(2) [data-testid="column"] .stButton button {
            padding: 20px 24px !important; font-size: 1.05rem !important; font-weight: 600 !important;
            min-height: 52px !important;
            background: #f5f0e6 !important; color: #3d4f42 !important;
            border: 2px solid #3d4f42 !important; border-radius: 14px !important;
            box-shadow: 0 2px 8px rgba(61,79,66,0.08) !important;
        }
        .block-container > div:nth-child(2) [data-testid="column"] .stButton button[kind="primary"] {
            background: #3d4f42 !important; color: #f5f0e6 !important;
            border-color: #2d3d2f !important;
        }
        .block-container > div:nth-child(2) [data-testid="column"] .stButton button:hover {
            box-shadow: 0 4px 14px rgba(61,79,66,0.18) !important; transform: translateY(-2px) !important;
            filter: none !important;
        }
    """

    button_css = """
        [data-testid="stButton"] button, .stButton button {
            transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important;
            border-radius: 14px !important;
        }
        [data-testid="stButton"] button:hover, .stButton button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(61,79,66,0.15) !important;
        }
        [data-testid="stButton"] button[kind="primary"], .stButton button[kind="primary"] {
            background: #3d4f42 !important; color: #f5f0e6 !important; border: 2px solid #2d3d2f !important;
        }
        [data-testid="stButton"] button[kind="secondary"], .stButton button[kind="secondary"] {
            background: #f5f0e6 !important; color: #3d4f42 !important; border: 2px solid #3d4f42 !important;
        }
    """

    st.markdown(
        f"<style>{hide_css}{theme_css}{page_theme}{anim_css}{layout_css}{nav_css}{button_css}</style>",
        unsafe_allow_html=True,
    )


def render_top_nav(current_page: str = ""):
    """Barre de navigation : logo + BioGuide + slogan, puis 3 grands boutons."""
    logo_src = _logo_data_url()
    img_html = (
        f'<img src="{logo_src}" alt="BioGuide" class="brand-logo" />'
        if logo_src
        else ""
    )
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 24px;">
            {img_html}
            <h1 class="brand-title" style="font-size: 1.75rem; font-weight: 700; margin: 0 0 6px 0;">BioGuide</h1>
            <p class="brand-slogan" style="font-size: 0.9rem; margin: 0;">{APP_SLOGAN}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    nav_items = [
        ("Les livres", "pages/1_Livres.py"),
        ("Recherche IA", "pages/2_Recherche_avec_IA.py"),
        ("À propos", "pages/4_A_propos.py"),
    ]
    cols = st.columns(3)
    for i, (label, target) in enumerate(nav_items):
        with cols[i]:
            is_current = current_page == target
            btn = st.button(
                label,
                key=f"nav_{label}",
                type="primary" if is_current else "secondary",
                use_container_width=True,
            )
            if btn:
                st.switch_page(target)
    st.divider()


def render_sidebar_nav(pages: list):
    """Affiche la navigation latérale (non utilisée si la barre est masquée)."""
    with st.sidebar:
        st.markdown("## BioGuide")
        st.caption("Remèdes par les plantes")
        st.divider()

        for label, target in pages:
            if st.button(label, key=f"nav_{label}", use_container_width=True):
                st.switch_page(target)

        st.divider()
        st.toggle("Mode sombre", key="dark_mode")


def render_disclaimer():
    """Affiche l'avertissement médical en bas de page."""
    st.divider()
    st.markdown(
        """
        <div class="disclaimer-box" style="padding: 16px 20px;">
        <strong>Avertissement médical</strong><br>
        Les informations proviennent de sources historiques et ne constituent pas un avis médical.
        Consultez toujours un professionnel de santé.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_warning(message: str, level: str = "warning"):
    """Affiche un encadré d'alerte (warning, danger ou info)."""
    dark = _get_dark_mode()
    if dark:
        colors = {
            "warning": {"bg": "#422006", "border": "#F59E0B", "text": "#fef3c7"},
            "danger": {"bg": "#450a0a", "border": "#EF4444", "text": "#fecaca"},
            "info": {"bg": "#0c1929", "border": "#3BA4F7", "text": "#bfdbfe"},
        }
    else:
        colors = {
            "warning": {"bg": "#f5f0e6", "border": "#c4a574", "text": "#2d3d2f"},
            "danger": {"bg": "#f5f0e6", "border": "#d4a5a8", "text": "#2d3d2f"},
            "info": {"bg": "#f5f0e6", "border": "#5f8f7a", "text": "#2d3d2f"},
        }
    style = colors.get(level, colors["warning"])
    st.markdown(
        f'<div style="background:{style["bg"]};border:2px solid {style["border"]};color:{style["text"]};padding:16px;border-radius:16px;margin:16px 0;">{message}</div>',
        unsafe_allow_html=True,
    )


def render_book_badge(book_id: str) -> str:
    """Retourne le HTML du badge coloré pour un identifiant d'ouvrage."""
    if book_id not in BOOK_INFO:
        return f"`{book_id}`"
    info = BOOK_INFO[book_id]
    return f'<span style="background:{info["color"]};color:white;padding:4px 10px;border-radius:8px;font-size:0.85em;font-weight:500;">{info["short_title"]}</span>'


def render_citation(book_id: str, page: int) -> str:
    """Retourne le HTML de la citation (badge + numéro de page)."""
    badge = render_book_badge(book_id)
    return f'{badge} <span class="citation-page">p. {page}</span>'


_GALLICA_OCR_DISCLAIMER = (
    "Le texte affiché peut comporter un certain nombre d'erreurs. "
    "En effet, le mode texte de ce document a été généré de façon automatique "
    "par un programme de reconnaissance optique de caractères (OCR)."
)


def clean_text_for_display(text: str) -> str:
    """Nettoie le texte OCR / JSON pour l'affichage."""
    if not text or not isinstance(text, str):
        return ""
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\\'", "'").replace('\\"', '"').replace("\\n", " ").replace("\\t", " ")
    text = re.sub(r',\s*"[^"]*OCR[^"]*"\s*:\s*"[^"]*"', " ", text, flags=re.IGNORECASE)
    text = re.sub(r',\s*"[a-zA-Z]+"\s*:\s*"[^"]*"', " ", text)
    text = text.replace(_GALLICA_OCR_DISCLAIMER, " ")
    for fragment in ["reconnaissance optique de caractères (OCR)", "généré de façon automatique", "peut comporter un certain nombre d'erreurs"]:
        if fragment.lower() in text.lower():
            text = re.sub(re.escape(fragment), " ", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip()


def render_result_card(passage: str, book_id: str, page: int, score: Optional[float] = None, show_score: bool = False, max_length: int = 300, result_index: Optional[int] = None):
    """Affiche une carte de résultat de recherche."""
    cleaned = clean_text_for_display(passage)
    st.markdown(render_citation(book_id, page), unsafe_allow_html=True)
    if show_score and score is not None:
        st.caption(f"Score : {score:.3f}")
    preview = cleaned[:max_length] + "..." if len(cleaned) > max_length else cleaned
    st.write(preview)
    if len(cleaned) > max_length:
        with st.expander("Voir plus"):
            st.write(cleaned)

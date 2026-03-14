"""
BioGuide - Design system healthcare premium
Couleurs: bleu médical #3BA4F7, teal #29C7AC
"""
import streamlit as st
from typing import Optional
import re

# Design tokens
COLORS = {
    "primary": "#3BA4F7",
    "secondary": "#29C7AC",
    "bg_main": "#F7FBFD",
    "bg_secondary": "#EEF6F8",
    "bg_card": "#FFFFFF",
    "text_main": "#1F2A37",
    "text_secondary": "#5B6B7A",
    "text_muted": "#8A97A6",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "error": "#EF4444",
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

# Slogan de l'app
APP_SLOGAN = "Des remèdes d'hier, une santé sans chimie."


def get_gallica_page_url(book_id: str, page: int) -> str:
    ark = BOOK_INFO.get(book_id, {}).get("ark", "")
    return f"https://gallica.bnf.fr/ark:/12148/{ark}/f{page}"


def _get_dark_mode() -> bool:
    return st.session_state.get("dark_mode", False) if "dark_mode" in st.session_state else False


def load_global_css(dark_mode: Optional[bool] = None, theme: str = "default"):
    """theme: default, rustic (Livres), hybrid (Recherche IA)"""
    if dark_mode is None:
        dark_mode = _get_dark_mode()

    # Masquer footer, sidebar et barre blanche en haut (header/decoration) qui cache les boutons
    hide_css = """
    footer { visibility: hidden; }
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    """

    if theme == "rustic":
        page_theme = """
        .stApp, [data-testid="stAppViewContainer"], .main .block-container {
            background: linear-gradient(135deg, #f5f0e6 0%, #e8dfd0 50%, #f0e9dc 100%) !important;
        }
        .main .block-container { font-family: Georgia, 'Times New Roman', serif !important; }
        .main .block-container p, .main .block-container span, .main .block-container div,
        .main .block-container label, [data-testid="stMarkdown"] p, [data-testid="stMarkdown"] span { color: #3d3529 !important; }
        .rustic-card { background: #faf6e8 !important; border: 2px solid #c4a574 !important; border-radius: 4px !important;
            box-shadow: 4px 4px 12px rgba(0,0,0,0.15), inset 0 0 0 1px rgba(196,165,116,0.3) !important;
            padding: 28px !important; margin: 28px 0 !important; }
        .rustic-title { font-family: Georgia, serif !important; color: #5c4a32 !important; font-size: 1.4rem !important; }
        .rustic-curtain { background: linear-gradient(90deg, #8b4513 0%, #a0522d 20%, #8b4513 50%, #a0522d 80%, #8b4513 100%) !important;
            padding: 16px 20px !important; border-radius: 2px !important; margin: 24px 0 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.2) !important; }
        a { color: #6b4e2e !important; text-decoration: underline !important; }
        """
    elif theme == "hybrid":
        page_theme = """
        .stApp, [data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #f0f4f8 0%, #e8eef5 100%) !important; }
        .main .block-container { background: transparent !important; padding-bottom: 140px !important; }
        .hybrid-card-old { background: #faf6e8 !important; border: 1px solid #c4a574 !important; border-radius: 8px !important; padding: 16px !important; margin: 12px 0 !important; font-family: Georgia, serif !important; color: #3d3529 !important; }
        .hybrid-card-new { background: rgba(59,164,247,0.08) !important; border: 1px solid rgba(59,164,247,0.3) !important; border-radius: 12px !important; padding: 16px !important; margin: 12px 0 !important; }
        .main .block-container p, .main .block-container span, .main .block-container div,
        .main .block-container label, [data-testid="stMarkdown"] p, [data-testid="stMarkdown"] span,
        [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span { color: #1F2A37 !important; }
        /* Style ChatGPT-like : barre fixe en bas, compacte, centrée, reste visible au scroll */
        [data-testid="stChatInput"] {
            position: fixed !important; bottom: 0 !important; left: 50% !important;
            transform: translateX(-50%) !important; width: 100% !important; max-width: 640px !important;
            padding: 16px 24px 24px !important;
            background: linear-gradient(180deg, transparent 0%, rgba(240,244,248,0.95) 15%, #f0f4f8 100%) !important;
            z-index: 999 !important;
        }
        [data-testid="stChatInput"] textarea {
            min-height: 52px !important; max-height: 120px !important;
            border-radius: 24px !important; border: 1px solid #d1d5db !important;
            padding: 14px 20px !important; font-size: 1rem !important;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
        }
        """
    else:
        page_theme = ""

    if dark_mode:
        theme_css = """
        .stApp { background: #0f1419; }
        [data-testid="stAppViewContainer"] { background: #0f1419; }
        .main .block-container { background: #0f1419; }
        [data-testid="stSidebar"] { background: #161d26; border-right: 1px solid #2a3544; }
        .main .block-container p, .main .block-container span, .main .block-container div,
        .main .block-container label, [data-testid="stMarkdown"] p, [data-testid="stMarkdown"] span,
        [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span, [data-testid="stChatMessage"] div,
        [data-testid="stCaptionContainer"], .stCaption { color: #e2e8f0 !important; }
        .hero-title { color: #3BA4F7 !important; }
        .hero-sub { color: #94a3b8 !important; }
        .stat-card { background: #161d26; border: 1px solid #2a3544; }
        .stat-value { color: #29C7AC !important; }
        .stat-label { color: #94a3b8 !important; }
        .disclaimer-box { background: #1e293b; border-left: 4px solid #F59E0B; color: #fef3c7 !important; }
        [data-testid="stChatInput"] textarea { background: #161d26 !important; color: #e2e8f0 !important; }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: #e2e8f0 !important; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 { color: #3BA4F7 !important; }
        .citation-page { color: #94a3b8 !important; }
        a { color: #60a5fa !important; }
        """
    else:
        theme_css = """
        .stApp { background: #F7FBFD; }
        [data-testid="stAppViewContainer"] { background: #F7FBFD; }
        .main .block-container { background: #F7FBFD; }
        [data-testid="stSidebar"] { background: #EEF6F8; border-right: 1px solid #dbeafe; }
        .hero-title { color: #1F2A37 !important; }
        .hero-sub { color: #5B6B7A !important; }
        .stat-card { background: #FFFFFF; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
        .stat-value { color: #3BA4F7 !important; }
        .stat-label { color: #5B6B7A !important; }
        .disclaimer-box { background: #fffbeb; border-left: 4px solid #F59E0B; color: #92400e; }
        .citation-page { color: #5B6B7A !important; }
        /* Liens */
        a { color: #3BA4F7 !important; }
        /* Chat */
        [data-testid="stChatInput"] { border-radius: 16px; }
        """

    # Animations subtiles
    anim_css = """
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .stat-card { animation: fadeInUp 0.25s ease-out; }
    """

    # Spacing: 4 8 12 16 24 32 40
    layout_css = """
        .block-container { padding: 40px 48px 48px; max-width: 960px; }
        .hero-section { text-align: center; padding: 48px 24px 40px; }
        .hero-title { font-size: 2rem; font-weight: 700; margin-bottom: 8px; letter-spacing: -0.02em; }
        .hero-sub { font-size: 1.05rem; margin-bottom: 4px; }
        .stat-card { padding: 24px; border-radius: 16px; text-align: center; margin-bottom: 20px;
                     transition: transform 0.2s ease, box-shadow 0.2s ease; }
        .stat-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(59,164,247,0.12); }
        .stat-value { font-size: 1.75rem; font-weight: 700; margin-bottom: 4px; }
        .stat-label { font-size: 0.9rem; }
        .content-card { background: #FFFFFF; border-radius: 16px; padding: 24px; margin: 28px 0;
                       box-shadow: 0 1px 3px rgba(0,0,0,0.06); border: 1px solid #e5e7eb; }
        .section-spacer { margin: 40px 0; }
    """

    # Top nav: grands boutons visibles, bien dégagés (barre blanche masquée)
    nav_css = """
        .block-container { padding-top: 32px !important; overflow: visible !important; }
        .block-container > div:first-child { margin-bottom: 20px !important; overflow: visible !important; }
        .block-container > div:nth-child(2) { margin-bottom: 28px !important; overflow: visible !important; }
        .block-container > div:nth-child(2) [data-testid="column"] { padding: 0 10px !important; overflow: visible !important; }
        .block-container > div:nth-child(2) [data-testid="column"] .stButton button {
            padding: 22px 28px !important; font-size: 1.2rem !important; font-weight: 700 !important;
            min-height: 56px !important; border: 2px solid rgba(0,0,0,0.12) !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.12) !important; color: white !important;
        }
        .block-container > div:nth-child(2) [data-testid="column"]:nth-child(1) .stButton button {
            background: #3BA4F7 !important; border-color: #2d8ad9 !important;
        }
        .block-container > div:nth-child(2) [data-testid="column"]:nth-child(2) .stButton button {
            background: #29C7AC !important; border-color: #1fa88e !important;
        }
        .block-container > div:nth-child(2) [data-testid="column"]:nth-child(3) .stButton button {
            background: #8B5CF6 !important; border-color: #7c3aed !important;
        }
        .block-container > div:nth-child(2) [data-testid="column"] .stButton button:hover {
            box-shadow: 0 4px 16px rgba(0,0,0,0.25) !important; transform: translateY(-2px) !important;
            filter: brightness(1.08);
        }
    """

    # Buttons: primary blue, subtle animations
    button_css = """
        [data-testid="stButton"] button, .stButton button {
            transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important;
            border-radius: 12px !important;
        }
        [data-testid="stButton"] button:hover, .stButton button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(59,164,247,0.25) !important;
        }
        [data-testid="stButton"] button:active, .stButton button:active {
            transform: translateY(0) !important;
        }
        [data-testid="stButton"] button[kind="primary"], .stButton button[kind="primary"] {
            background: #3BA4F7 !important; border: none !important;
        }
        [data-testid="stButton"] button[kind="primary"]:hover {
            box-shadow: 0 4px 16px rgba(59,164,247,0.35) !important;
        }
    """

    st.markdown(
        f"<style>{hide_css}{theme_css}{page_theme}{anim_css}{layout_css}{nav_css}{button_css}</style>",
        unsafe_allow_html=True,
    )


def render_top_nav(current_page: str = ""):
    """Barre de navigation : BioGuide + slogan, puis 3 grands boutons."""
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 24px;">
            <h1 style="font-size: 1.75rem; font-weight: 700; color: #1F2A37; margin: 0 0 6px 0;">BioGuide</h1>
            <p style="font-size: 0.9rem; color: #5B6B7A; margin: 0;">{APP_SLOGAN}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    nav_items = [
        ("Les Livres", "pages/1_Livres.py"),
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
    st.divider()
    st.markdown(
        """
        <div class="disclaimer-box" style="padding: 16px 20px; border-radius: 12px;">
        <strong>Avertissement médical</strong><br>
        Les informations proviennent de sources historiques et ne constituent pas un avis médical.
        Consultez toujours un professionnel de santé.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_warning(message: str, level: str = "warning"):
    dark = _get_dark_mode()
    if dark:
        colors = {
            "warning": {"bg": "#422006", "border": "#F59E0B", "text": "#fef3c7"},
            "danger": {"bg": "#450a0a", "border": "#EF4444", "text": "#fecaca"},
            "info": {"bg": "#0c1929", "border": "#3BA4F7", "text": "#bfdbfe"},
        }
    else:
        colors = {
            "warning": {"bg": "#fffbeb", "border": "#F59E0B", "text": "#92400e"},
            "danger": {"bg": "#fef2f2", "border": "#EF4444", "text": "#991b1b"},
            "info": {"bg": "#eff6ff", "border": "#3BA4F7", "text": "#1e40af"},
        }
    style = colors.get(level, colors["warning"])
    st.markdown(
        f'<div style="background:{style["bg"]};border-left:4px solid {style["border"]};color:{style["text"]};padding:16px;border-radius:12px;margin:16px 0;">{message}</div>',
        unsafe_allow_html=True,
    )


def render_book_badge(book_id: str) -> str:
    if book_id not in BOOK_INFO:
        return f"`{book_id}`"
    info = BOOK_INFO[book_id]
    return f'<span style="background:{info["color"]};color:white;padding:4px 10px;border-radius:8px;font-size:0.85em;font-weight:500;">{info["short_title"]}</span>'


def render_citation(book_id: str, page: int) -> str:
    badge = render_book_badge(book_id)
    return f'{badge} <span class="citation-page">p. {page}</span>'


_GALLICA_OCR_DISCLAIMER = (
    "Le texte affiché peut comporter un certain nombre d'erreurs. "
    "En effet, le mode texte de ce document a été généré de façon automatique "
    "par un programme de reconnaissance optique de caractères (OCR)."
)


def clean_text_for_display(text: str) -> str:
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
    cleaned = clean_text_for_display(passage)
    st.markdown(render_citation(book_id, page), unsafe_allow_html=True)
    if show_score and score is not None:
        st.caption(f"Score : {score:.3f}")
    preview = cleaned[:max_length] + "..." if len(cleaned) > max_length else cleaned
    st.write(preview)
    if len(cleaned) > max_length:
        with st.expander("Voir plus"):
            st.write(cleaned)

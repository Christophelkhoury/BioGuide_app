"""
Reusable UI components for the Streamlit app.
"""
import streamlit as st
from typing import Optional
import uuid
import re
import html

# Book metadata mapping
BOOK_INFO = {
    "plantes": {
        "title": "La santé par les plantes",
        "short_title": "Plantes",
        "ark": "bpt6k5688257m",
        "source_url": "https://gallica.bnf.fr/ark:/12148/bpt6k5688257m",
        "color": "#2E7D32",  # Green
    },
    "pauvres": {
        "title": "Le médecin des pauvres",
        "short_title": "Pauvres",
        "ark": "bpt6k5791358q",
        "source_url": "https://gallica.bnf.fr/ark:/12148/bpt6k5791358q",
        "color": "#1565C0",  # Blue
    },
}


def load_global_css():
    """Load global responsive CSS styles."""
    st.markdown(
        """
        <style>
        /* ===== GLOBAL RESPONSIVE STYLES ===== */
        
        /* Base spacing system */
        :root {
            --spacing-xs: 0.5rem;
            --spacing-sm: 1rem;
            --spacing-md: 1.5rem;
            --spacing-lg: 2rem;
            --spacing-xl: 3rem;
            --border-radius: 8px;
            --border-radius-lg: 12px;
        }
        
        /* Main container */
        .main {
            padding: var(--spacing-md) var(--spacing-sm);
        }
        
        /* Responsive typography */
        h1 {
            font-size: clamp(1.75rem, 5vw, 2.5rem);
            margin-bottom: var(--spacing-sm);
        }
        
        h2 {
            font-size: clamp(1.5rem, 4vw, 2rem);
            margin-bottom: var(--spacing-sm);
        }
        
        h3 {
            font-size: clamp(1.25rem, 3vw, 1.5rem);
            margin-bottom: var(--spacing-xs);
        }
        
        /* Hero section - responsive */
        .hero {
            text-align: center;
            padding: var(--spacing-lg) var(--spacing-sm);
            margin-bottom: var(--spacing-lg);
        }
        
        .hero h1 {
            font-size: clamp(2rem, 6vw, 3rem);
            font-weight: 600;
            color: #111827; /* neutral heading */
            margin-bottom: var(--spacing-xs);
            line-height: 1.2;
        }
        
        .hero p {
            font-size: clamp(1rem, 3vw, 1.25rem);
            color: #666;
            margin-bottom: var(--spacing-sm);
            line-height: 1.5;
        }
        
        /* Feature cards - responsive grid */
        .feature-card {
            background-color: #F8F9FA;
            border: 1px solid #DEE2E6;
            border-radius: var(--border-radius-lg);
            padding: var(--spacing-md);
            margin-bottom: var(--spacing-md);
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
            height: 100%;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .feature-card h2 {
            font-size: clamp(2rem, 5vw, 3rem);
            margin: var(--spacing-sm) 0;
        }
        
        .feature-card h3 {
            color: #2563EB; /* medical blue accent */
            margin-top: var(--spacing-sm);
            margin-bottom: var(--spacing-xs);
        }
        
        .feature-card p {
            font-size: clamp(0.9rem, 2vw, 1rem);
            line-height: 1.6;
            color: #555;
        }
        
        /* Stats boxes - responsive */
        .stat-box {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            color: #111827;
            padding: var(--spacing-md);
            border-radius: var(--border-radius);
            text-align: center;
            margin-bottom: var(--spacing-sm);
            box-shadow: 0 1px 2px rgba(15,23,42,0.06);
        }
        
        .stat-number {
            font-size: clamp(1.75rem, 5vw, 2.5rem);
            font-weight: 700;
            margin-bottom: var(--spacing-xs);
            line-height: 1.2;
        }
        
        .stat-label {
            font-size: clamp(0.85rem, 2vw, 0.9rem);
            opacity: 0.95;
            line-height: 1.4;
        }
        
        /* Result cards - responsive */
        .result-card {
            background-color: #F8F9FA;
            border: 1px solid #DEE2E6;
            border-radius: var(--border-radius);
            padding: var(--spacing-md);
            margin: var(--spacing-sm) 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .result-card-header {
            margin-bottom: var(--spacing-xs);
            display: flex;
            flex-wrap: wrap;
            gap: var(--spacing-xs);
            align-items: center;
        }
        
        .result-card-text {
            color: #333;
            line-height: 1.6;
            margin-top: var(--spacing-xs);
            font-size: clamp(0.9rem, 2vw, 1rem);
        }
        
        /* Badges - responsive */
        .book-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: clamp(0.75rem, 2vw, 0.85em);
            font-weight: 500;
            white-space: nowrap;
        }
        
        /* Citation - responsive */
        .citation {
            display: inline-flex;
            align-items: center;
            gap: var(--spacing-xs);
            flex-wrap: wrap;
            font-size: clamp(0.85rem, 2vw, 0.9em);
        }
        
        /* Warning boxes - responsive */
        .warning-box {
            padding: var(--spacing-md);
            margin: var(--spacing-md) 0;
            border-radius: var(--border-radius);
            font-size: clamp(0.95rem, 2.5vw, 1.05em);
            line-height: 1.6;
        }
        
        .disclaimer-box {
            padding: var(--spacing-md);
            margin: var(--spacing-md) 0;
            border-radius: var(--border-radius);
            font-size: clamp(0.9rem, 2vw, 1rem);
            line-height: 1.6;
        }
        
        /* Responsive containers */
        .container {
            width: 100%;
            padding: 0 var(--spacing-sm);
        }
        
        /* Sidebar adjustments for mobile */
        @media (max-width: 768px) {
            .main {
                padding: var(--spacing-sm);
            }
            
            .hero {
                padding: var(--spacing-md) var(--spacing-sm);
            }
            
            .feature-card {
                margin-bottom: var(--spacing-md);
            }
            
            .stat-box {
                margin-bottom: var(--spacing-sm);
            }
        }
        
        /* Tablet adjustments */
        @media (min-width: 769px) and (max-width: 1024px) {
            .hero h1 {
                font-size: 2.5rem;
            }
        }
        
        /* Desktop - maintain spacing */
        @media (min-width: 1025px) {
            .main {
                padding: var(--spacing-lg) var(--spacing-md);
            }
        }
        
        /* Ensure buttons are touch-friendly on mobile */
        button {
            min-height: 44px;
            padding: var(--spacing-xs) var(--spacing-md);
        }
        
        /* Improve text input on mobile */
        input[type="text"], textarea {
            font-size: clamp(1rem, 3vw, 1.1rem);
            padding: var(--spacing-xs) var(--spacing-sm);
        }
        
        /* Consistent spacing for sections */
        section {
            margin-bottom: var(--spacing-lg);
        }
        
        /* Divider spacing */
        hr {
            margin: var(--spacing-lg) 0;
        }
        
        /* Expander spacing */
        .streamlit-expanderHeader {
            font-size: clamp(1rem, 2.5vw, 1.1rem);
        }
        
        /* Streamlit column gaps - fallback if gap parameter not supported */
        [data-testid="column"] {
            padding: 0 var(--spacing-xs);
        }
        
        /* Responsive container padding */
        .block-container {
            padding-top: var(--spacing-md);
            padding-bottom: var(--spacing-md);
        }
        
        /* Sidebar responsive adjustments */
        [data-testid="stSidebar"] {
            min-width: 250px;
        }
        
        @media (max-width: 768px) {
            [data-testid="stSidebar"] {
                min-width: 200px;
            }
            
            .block-container {
                padding-left: var(--spacing-sm);
                padding-right: var(--spacing-sm);
            }
        }
        
        /* Ensure proper spacing between elements */
        .element-container {
            margin-bottom: var(--spacing-sm);
        }
        
        /* Responsive metric cards */
        [data-testid="stMetricValue"] {
            font-size: clamp(1.5rem, 4vw, 2rem);
        }
        
        [data-testid="stMetricLabel"] {
            font-size: clamp(0.85rem, 2vw, 0.95rem);
        }
        
        /* Better spacing for info/warning boxes */
        .stAlert {
            margin-bottom: var(--spacing-md);
        }
        
        /* Responsive table if used */
        table {
            font-size: clamp(0.85rem, 2vw, 1rem);
        }
        
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_book_badge(book_id: str) -> str:
    """Render a styled badge for a book."""
    if book_id not in BOOK_INFO:
        return f"`{book_id}`"
    
    info = BOOK_INFO[book_id]
    color = info["color"]
    title = info["short_title"]
    
    return f'<span class="book-badge" style="background-color: {color}; color: white;">{title}</span>'


def render_citation(book_id: str, page: int) -> str:
    """Render a citation badge with book and page."""
    badge = render_book_badge(book_id)
    return f'<span class="citation">{badge} <span style="color: #666;">p. {page}</span></span>'


def render_disclaimer():
    """Render the medical disclaimer."""
    st.markdown("---")
    st.markdown(
        """
        <div class="disclaimer-box" style="background-color: #FEF3C7; border-left: 4px solid #D97706;">
        <strong>Avertissement médical</strong><br>
        Les informations présentées dans cette application proviennent de sources historiques et ne constituent 
        <strong>pas un avis médical professionnel</strong>. Consultez toujours un professionnel de santé qualifié 
        pour tout problème médical. Ne remplacez jamais un traitement médical par des remèdes traditionnels sans 
        consultation préalable.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_warning(message: str, level: str = "warning"):
    """Render a prominent warning banner."""
    colors = {
        "warning": {"bg": "#FEF3C7", "border": "#D97706", "label": "Avertissement"},
        "danger": {"bg": "#FEE2E2", "border": "#B91C1C", "label": "Alerte importante"},
        "info": {"bg": "#DBEAFE", "border": "#1D4ED8", "label": "Information"},
    }
    
    style = colors.get(level, colors["warning"])
    
    st.markdown(
        f"""
        <div class="warning-box" style="background-color: {style['bg']}; border-left: 6px solid {style['border']};">
        <strong>{style['label']}</strong><br>{message}
        </div>
        """,
        unsafe_allow_html=True,
    )


# Gallica OCR metadata / disclaimer to strip from displayed text
_GALLICA_OCR_DISCLAIMER = (
    "Le texte affiché peut comporter un certain nombre d'erreurs. "
    "En effet, le mode texte de ce document a été généré de façon automatique "
    "par un programme de reconnaissance optique de caractères (OCR)."
)


def clean_text_for_display(text: str) -> str:
    """Clean text for display: remove HTML, JSON-like metadata, and Gallica OCR boilerplate."""
    if not text or not isinstance(text, str):
        return ""
    # Remove HTML tags
    text = re.sub(r'<br\s*/?>', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    # Fix escaped characters
    text = text.replace("\\'", "'").replace('\\"', '"').replace('\\n', ' ').replace('\\t', ' ')
    # Remove JSON-like Gallica metadata: ","key":"value" or similar
    text = re.sub(r',\s*"[^"]*OCR[^"]*"\s*:\s*"[^"]*"', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r',\s*"[a-zA-Z]+"\s*:\s*"[^"]*"', ' ', text)
    # Remove the standard Gallica OCR disclaimer (any case)
    text = text.replace(_GALLICA_OCR_DISCLAIMER, ' ')
    # Also remove truncated or partial disclaimer
    for fragment in [
        "reconnaissance optique de caractères (OCR)",
        "généré de façon automatique",
        "peut comporter un certain nombre d'erreurs",
    ]:
        if fragment.lower() in text.lower():
            text = re.sub(re.escape(fragment), ' ', text, flags=re.IGNORECASE)
    # Collapse spaces and trim
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def render_result_card(
    passage: str,
    book_id: str,
    page: int,
    score: Optional[float] = None,
    show_score: bool = False,
    max_length: int = 300,
    result_index: Optional[int] = None,
):
    """Render a search result card using plain text widgets (no raw HTML in content)."""
    cleaned_passage = clean_text_for_display(passage)

    # Citation line (book + page)
    st.markdown(render_citation(book_id, page), unsafe_allow_html=True)

    # Optional score
    if show_score and score is not None:
        st.caption(f"Score TF‑IDF : {score:.3f}")

    # Truncate for preview
    is_truncated = len(cleaned_passage) > max_length
    preview = cleaned_passage
    if is_truncated:
        truncated = cleaned_passage[:max_length]
        last_space = truncated.rfind(" ")
        if last_space > max_length * 0.8:
            preview = truncated[:last_space] + "..."
        else:
            preview = truncated + "..."

    # Main text preview as plain text
    st.write(preview)

    # Full text expander
    if is_truncated:
        with st.expander("Afficher le passage complet"):
            st.write(cleaned_passage)

    # Copy button – unique key
    col1, _ = st.columns([1, 4])
    with col1:
        if result_index is not None:
            button_key = f"copy_result_{result_index}"
        else:
            unique_id = str(uuid.uuid4())[:8]
            button_key = f"copy_{book_id}_{page}_{unique_id}"

        if st.button("Copier l'extrait", key=button_key):
            st.code(cleaned_passage, language=None)
            st.success("Extrait copié.")

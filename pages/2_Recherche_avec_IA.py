"""
BioGuide - Recherche avec IA (chat conversationnel)
UI mix ancien/futur : passage des livres d'époque à l'IA moderne.
"""
import streamlit as st
from src.search import SearchEngine
from src.safety import check_red_flags, check_risk_keywords, get_red_flag_message, get_risk_notice
from src.ui_components import (
    BOOK_INFO,
    render_disclaimer,
    render_warning,
    load_global_css,
    render_top_nav,
    clean_text_for_display,
    get_gallica_page_url,
)
from src.assistant_llm import extract_symptoms, synthesize_with_sources, is_llm_available

# Cache search engine - pre-warmed on page load to avoid "Running..." message
@st.cache_resource
def get_cached_search_engine():
    engine = SearchEngine()
    engine.build_index(None)
    return engine


st.set_page_config(
    page_title="BioGuide — Recherche avec IA",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_global_css(theme="hybrid")
render_top_nav("pages/2_Recherche_avec_IA.py")

st.markdown("")
st.markdown("## Recherche avec IA")
st.caption("Décrivez vos symptômes. L'assistant cherche dans les ouvrages et vous propose une synthèse avec les sources.")

# Initialize chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Pre-warm search engine cache (runs once, avoids "Running get_cached_search_engine" during chat)
get_cached_search_engine()

# Display chat history
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            st.markdown("**Sources :**")
            for s in msg["sources"]:
                st.markdown(f'- <a href="{s["url"]}" target="_blank" rel="noopener">{s["label"]}</a>', unsafe_allow_html=True)
            st.caption("Si un lien ne s'ouvre pas, Gallica peut être temporairement lent. Réessayez ou copiez l'URL.")

# Chat input - barre fixe en bas (style ChatGPT)
if prompt := st.chat_input("Décrivez vos symptômes ou posez votre question...", width=640):
    # Add user message
    st.session_state.chat_messages.append({"role": "user", "content": prompt})

    # Safety: red flags
    has_red_flags, red_flag_keywords = check_red_flags(prompt)
    if has_red_flags:
        warning_content = get_red_flag_message(red_flag_keywords) + "\n\n**Cette application ne peut pas fournir de diagnostic médical.**\n\nPour des symptômes graves ou urgents, consultez immédiatement :\n- **15** (SAMU) pour les urgences médicales\n- **112** (numéro d'urgence européen)"
        with st.chat_message("assistant"):
            render_warning(get_red_flag_message(red_flag_keywords), level="danger")
            st.markdown(
                "**Cette application ne peut pas fournir de diagnostic médical.**\n\n"
                "Pour des symptômes graves ou urgents, consultez immédiatement :\n"
                "- **15** (SAMU) pour les urgences médicales\n"
                "- **112** (numéro d'urgence européen)"
            )
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": warning_content,
            "sources": [],
        })
        st.rerun()

    has_risks, _ = check_risk_keywords(prompt)

    # Process with LLM
    with st.chat_message("assistant"):
        if has_risks:
            render_warning(get_risk_notice([]), level="info")
        with st.spinner("Analyse en cours..."):
            try:
                # 1. Extract symptoms (may fail if no API credits)
                symptoms = extract_symptoms(prompt)
                if not symptoms:
                    symptoms = [prompt.strip()]

                # 2. Search for each symptom
                engine = get_cached_search_engine()
                passages_by_symptom = {}
                for symptom in symptoms:
                    results = engine.search(symptom, top_k=4)
                    passages_by_symptom[symptom] = [
                        (book_id, page, clean_text_for_display(text))
                        for book_id, page, text, _ in results
                    ]

                # 3. Check if any results
                total_passages = sum(len(p) for p in passages_by_symptom.values())
                if total_passages == 0:
                    no_remedy_msg = (
                        "Aucun remède pertinent trouvé dans les ouvrages pour vos symptômes. "
                        "Consultez un professionnel de santé ou les urgences (15, 112) si nécessaire."
                    )
                    render_warning(no_remedy_msg, level="danger")
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": no_remedy_msg,
                        "sources": [],
                    })
                    st.rerun()

                # 4. Synthesize with sources
                response, api_error = synthesize_with_sources(
                    symptoms,
                    passages_by_symptom,
                    get_gallica_page_url,
                )

                if response:
                    st.markdown(response)
                    content_to_store = response
                else:
                    # API failed - afficher l'erreur précise + extraits en fallback
                    st.error(f"**L'assistant IA n'a pas pu répondre.** {api_error or 'Erreur inconnue.'}")
                    st.markdown("### Extraits trouvés")
                    for symptom in symptoms:
                        passages = passages_by_symptom.get(symptom, [])
                        if passages:
                            st.markdown(f"**{symptom}**")
                            for book_id, page, text in passages[:3]:
                                url = get_gallica_page_url(book_id, page)
                                title = BOOK_INFO.get(book_id, {}).get("title", book_id)
                                st.markdown(f'- <a href="{url}" target="_blank" rel="noopener">{title}, p. {page}</a>', unsafe_allow_html=True)
                                st.caption(text[:200] + "..." if len(text) > 200 else text)
                            st.markdown("")
                    content_to_store = (
                        f"L'assistant IA n'a pas pu répondre. {api_error or 'Erreur inconnue.'} "
                        "Extraits trouvés affichés ci-dessus."
                    )

                # 5. Build sources list (unique pages)
                seen = set()
                sources = []
                for symptom in symptoms:
                    for book_id, page, _ in passages_by_symptom.get(symptom, []):
                        key = (book_id, page)
                        if key not in seen:
                            seen.add(key)
                            title = BOOK_INFO.get(book_id, {}).get("title", book_id)
                            sources.append({
                                "label": f"{title}, page {page}",
                                "url": get_gallica_page_url(book_id, page),
                            })

                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": content_to_store,
                    "sources": sources,
                })

            except Exception as e:
                st.error(f"Erreur : {e}")
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": str(e),
                    "sources": [],
                })

    st.rerun()

# Empty state
if not st.session_state.chat_messages:
    st.markdown("")
    st.markdown("Décrivez vos symptômes dans la barre de saisie en bas de l'écran.")
    st.caption("Exemples : maux de tête, fièvre, remède contre la toux")

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
render_disclaimer()

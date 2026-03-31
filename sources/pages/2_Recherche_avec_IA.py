#Projet : BioGuide
#Auteurs : Christophe El Khoury, Tia Kahil, Alaa Hamdan
"""Page de recherche conversationnelle dans les ouvrages indexés."""
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
from src.assistant_llm import (
    extract_symptoms,
    is_usage_followup_question,
    synthesize_followup,
    synthesize_with_sources,
)


def _dedupe_passages(passages):
    """Dédoublonne les passages par couple (livre, page)."""
    seen = set()
    out = []
    for item in passages:
        if len(item) < 3:
            continue
        book_id, page, text = item[0], item[1], item[2]
        key = (book_id, page)
        if key not in seen:
            seen.add(key)
            out.append((book_id, page, text))
    return out


@st.cache_resource
def get_cached_search_engine():
    """Construit et met en cache le moteur de recherche TF-IDF."""
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
st.markdown(
    """
    <div class="hybrid-intro">
        <h2 style="margin: 0 0 8px 0;">Recherche avec IA</h2>
        <p style="margin: 0; color: #2d3d2f;">
            Décrivez vos symptômes. L'assistant cherche dans les ouvrages et vous propose une synthèse avec les sources.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

get_cached_search_engine()

_USAGE_SEARCH_SUFFIX = (
    "préparation infusion décoction teinture posologie emploi utilisation dose prendre appliquer macération"
)

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            st.markdown("**Sources :**")
            for s in msg["sources"]:
                st.markdown(f'- <a href="{s["url"]}" target="_blank" rel="noopener">{s["label"]}</a>', unsafe_allow_html=True)
            st.caption("Si un lien ne s'ouvre pas, Gallica peut être temporairement lent. Réessayez ou copiez l'URL.")

if prompt := st.chat_input("Décrivez vos symptômes ou posez votre question...", width=640):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})

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

    with st.chat_message("assistant"):
        if has_risks:
            render_warning(get_risk_notice([]), level="info")
        with st.spinner("Analyse en cours..."):
            try:
                is_followup_turn = False
                ctx = st.session_state.get("chat_search_context")
                followup = bool(ctx) and is_usage_followup_question(prompt, True)

                if followup:
                    is_followup_turn = True
                    symptoms = list(ctx["symptoms"])
                    passages_by_symptom = {
                        k: list(v) for k, v in ctx["passages_by_symptom"].items()
                    }
                    engine = get_cached_search_engine()
                    for symptom in symptoms:
                        usage_query = f"{symptom} {_USAGE_SEARCH_SUFFIX}"
                        results = engine.search(usage_query, top_k=4)
                        extra = [
                            (book_id, page, clean_text_for_display(text))
                            for book_id, page, text, _ in results
                        ]
                        prev = passages_by_symptom.get(symptom, [])
                        passages_by_symptom[symptom] = _dedupe_passages(prev + extra)

                    total_passages = sum(len(p) for p in passages_by_symptom.values())
                    if total_passages == 0:
                        no_ctx = (
                            "Je n'ai plus de contexte sur les remèdes précédents. "
                            "Reformulez votre symptôme pour relancer une recherche."
                        )
                        render_warning(no_ctx, level="info")
                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": no_ctx,
                            "sources": [],
                        })
                        st.rerun()

                    prior_summary = ""
                    for msg in reversed(st.session_state.chat_messages[:-1]):
                        if msg["role"] == "assistant" and (msg.get("content") or "").strip():
                            prior_summary = msg["content"].strip()
                            break

                    response, api_error = synthesize_followup(
                        prompt,
                        symptoms,
                        prior_summary,
                        passages_by_symptom,
                        get_gallica_page_url,
                    )
                else:
                    st.session_state.pop("chat_search_context", None)
                    symptoms = extract_symptoms(prompt)
                    if not symptoms:
                        symptoms = [prompt.strip()]

                    engine = get_cached_search_engine()
                    passages_by_symptom = {}
                    for symptom in symptoms:
                        results = engine.search(symptom, top_k=4)
                        passages_by_symptom[symptom] = [
                            (book_id, page, clean_text_for_display(text))
                            for book_id, page, text, _ in results
                        ]

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

                    response, api_error = synthesize_with_sources(
                        symptoms,
                        passages_by_symptom,
                        get_gallica_page_url,
                    )

                if response:
                    st.markdown(response)
                    content_to_store = response
                else:
                    st.error(f"**L'assistant n'a pas pu répondre.** {api_error or 'Erreur inconnue.'}")
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
                        f"L'assistant n'a pas pu répondre. {api_error or 'Erreur inconnue.'} "
                        "Extraits trouvés affichés ci-dessus."
                    )

                sources = []
                if not is_followup_turn:
                    seen = set()
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

                if response and total_passages > 0:
                    st.session_state["chat_search_context"] = {
                        "symptoms": list(symptoms),
                        "passages_by_symptom": {
                            k: list(v) for k, v in passages_by_symptom.items()
                        },
                    }

            except Exception as e:
                st.error(f"Erreur : {e}")
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": str(e),
                    "sources": [],
                })

    st.rerun()

if not st.session_state.chat_messages:
    st.markdown("")
    st.markdown("Décrivez vos symptômes dans la barre de saisie en bas de l'écran.")
    st.caption("Exemples : maux de tête, fièvre, remède contre la toux")

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
render_disclaimer()

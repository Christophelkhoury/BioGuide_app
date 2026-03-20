"""
Optional LLM integration to reformulate search results into a clear, contextual answer.
Uses an OpenAI-compatible API (OpenAI, Azure, or local endpoint).
"""
import json
import os
import re
from typing import List, Optional, Tuple

# --- Détection question de suivi (usage / préparation) vs nouveau symptôme ---
# Inclut fautes courantes (ex. « consome ») et synonymes (boire, ingérer…)
_FOLLOWUP_USAGE_RE = re.compile(
    r"\b(comment|comment je|comment on|comment les|comment la|comment l')\b.*\b("
    r"utiliser|prendre|employer|appliquer|préparer|faire|poser|doser|"
    r"consommer|consomme|consommation|boire|manger|ingérer|ingere|avaler|ingestion)\b|"
    r"\b(utilisation|mode d'?emploi|posologie|dosage|dose|combien|quand (prendre|boire|appliquer)|à quelle heure|durée|fréquence)\b|"
    r"\b(préparer|préparation|infusion|décoction|teinture|macérer|bouillir|laisser reposer)\b|"
    r"\b(plus de détails|plus précis|explique|expliquez|détaille|concrètement|en pratique)\b|"
    r"\b(comment ça marche|ça s'?utilise|ça se prend|comment faire)\b|"
    r"\b(et pour|pour la dose|les doses)\b|"
    r"\b(est[- ]ce que|est ce que)\b.*\b(consommer|consomme|prendre|utiliser|boire|préparer)\b|"
    r"\b(doivent|doit|peut[- ]on|faut[- ]il|dois[- ]je)\b.*\b(prendre|utiliser|consommer|consomme|boire)\b",
    re.IGNORECASE,
)

# Question sur des plantes / remèdes déjà cités (sans verbe exact du bloc ci-dessus)
_FOLLOWUP_LOOSE_Q_RE = re.compile(
    r"\b(comment|quel|quelle|quels|quelles|combien)\b",
    re.IGNORECASE,
)
_FOLLOWUP_PLANT_OR_REMEDY_RE = re.compile(
    r"\b(romarin|rosier|sauge|thym|joubarbe|plante|plantes|feuille|fleur|tisane|infusion|"
    r"décoction|teinture|herbe|remède|mélange|ingrédient)\b",
    re.IGNORECASE,
)

_NEW_SYMPTOM_RE = re.compile(
    r"\b(j'ai mal|j'ai la fièvre|j'ai de la fièvre|j'ai des maux|j'ai une douleur|j'ai du mal|je souffre|je me sens mal|"
    r"mal (à|au|aux|à la)\s|maux de|douleur (au|à|aux)\s|fièvre|touss|toux|nausée|vomis|diarrhée|constipation|brûlure|essouffl)\b|"
    r"\b(depuis hier|depuis ce matin|depuis \d+ jours?)\b",
    re.IGNORECASE,
)


def is_usage_followup_question(message: str, has_prior_search_context: bool) -> bool:
    """
    True if the user likely asks how to use / prepare remedies from the previous answer,
    and not a brand-new symptom description.
    """
    if not has_prior_search_context or not (message or "").strip():
        return False
    text = message.strip()
    if _NEW_SYMPTOM_RE.search(text):
        return False
    if _FOLLOWUP_USAGE_RE.search(text):
        return True
    # Phrases du type « comment … romarin / sauge » sans verbe listé plus haut
    if (
        len(text) <= 520
        and _FOLLOWUP_LOOSE_Q_RE.search(text)
        and _FOLLOWUP_PLANT_OR_REMEDY_RE.search(text)
    ):
        return True
    return False


# Passage format: (book_id, page, cleaned_text); source_label = "Titre du livre, p. N"
SYSTEM_PROMPT = """Tu es un assistant qui présente des remèdes historiques à base de plantes, à partir d'extraits d'ouvrages français numérisés (Gallica).
Règles strictes :
- Utilise UNIQUEMENT les informations contenues dans les extraits fournis. N'invente rien.
- Réponds en français, de façon claire et structurée (paragraphes courts ou listes à puces).
- Reformule et explique le contenu pour que ce soit compréhensible (contexte, usage, préparation si mentionné).
- Pour chaque information importante, indique brièvement la source (ex. "Selon La santé par les plantes, p. 42...").
- Rappelle que ces informations sont historiques et ne remplacent pas un avis médical."""

USER_PROMPT_TEMPLATE = """Question de l'utilisateur : {query}

Extraits des ouvrages (à utiliser comme seule base pour ta réponse) :

{excerpts}

Fournis une réponse reformulée et bien expliquée, en t'appuyant uniquement sur ces extraits."""


def _get_api_key() -> Optional[str]:
    """Get API key from environment or Streamlit secrets."""
    key = os.environ.get("OPENAI_API_KEY") or ""
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("OPENAI_API_KEY") or ""
        except Exception:
            return None
    key = (key or "").strip()
    if key and key != "VOTRE_CLE_ICI":
        return key
    return None


def _format_excerpts(passages: List[tuple], source_labels: List[str]) -> str:
    """Format (book_id, page, text) list with source labels for the prompt."""
    lines = []
    for i, ((book_id, page, text), label) in enumerate(zip(passages, source_labels), 1):
        lines.append(f"[Extrait {i} — {label}]\n{text.strip()}\n")
    return "\n".join(lines)


def reformulate_answer(
    query: str,
    passages: List[tuple],
    source_labels: List[str],
    model: str = "gpt-4o-mini",
    api_base: Optional[str] = None,
) -> Optional[str]:
    """
    Call an OpenAI-compatible LLM to reformulate and explain the answer from the given passages.

    Args:
        query: User question.
        passages: List of (book_id, page, cleaned_text).
        source_labels: List of display strings like "La santé par les plantes, p. 42".
        model: Model name (e.g. gpt-4o-mini, gpt-4o).
        api_base: Optional API base URL for compatible endpoints.

    Returns:
        Reformulated answer text, or None if API is unavailable or call fails.
    """
    if not passages or len(passages) != len(source_labels):
        return None

    api_key = _get_api_key()
    if not api_key:
        return None

    excerpts_text = _format_excerpts(passages, source_labels)
    user_content = USER_PROMPT_TEMPLATE.format(query=query, excerpts=excerpts_text)

    try:
        from openai import OpenAI
        kwargs = {"api_key": api_key}
        if api_base:
            kwargs["base_url"] = api_base
        client = OpenAI(**kwargs)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            max_tokens=1024,
            temperature=0.3,
        )
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
    except Exception:
        pass
    return None


def is_llm_available() -> bool:
    """Return True if an API key is configured for the LLM."""
    return _get_api_key() is not None


# --- Symptom extraction (for chat mode) ---
EXTRACT_SYMPTOMS_SYSTEM = """Tu es un assistant médical qui extrait les symptômes ou problèmes de santé d'un message utilisateur.
Retourne UNIQUEMENT un tableau JSON de chaînes, une par symptôme. Exemple: ["mal de tête", "fièvre"].
Si le message ne décrit aucun symptôme clair, retourne ["message"] pour traiter le message entier comme une requête.
Réponds uniquement avec le JSON, sans texte avant ou après."""

EXTRACT_SYMPTOMS_USER = """Message de l'utilisateur: "{message}"
Liste des symptômes ou problèmes de santé (JSON array):"""


def extract_symptoms(user_message: str, model: str = "gpt-4o-mini", api_base: Optional[str] = None) -> List[str]:
    """
    Extract individual symptoms from a user message.
    Returns a list of symptom strings to search for independently.
    """
    api_key = _get_api_key()
    if not api_key or not (user_message or "").strip():
        return [user_message.strip()] if user_message else []

    try:
        from openai import OpenAI
        kwargs = {"api_key": api_key}
        if api_base:
            kwargs["base_url"] = api_base
        client = OpenAI(**kwargs)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": EXTRACT_SYMPTOMS_SYSTEM},
                {"role": "user", "content": EXTRACT_SYMPTOMS_USER.format(message=user_message.strip())},
            ],
            max_tokens=256,
            temperature=0,
            timeout=30.0,
        )
        if not response.choices or not response.choices[0].message.content:
            return [user_message.strip()]
        raw = response.choices[0].message.content.strip()
        # Handle markdown code blocks
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        arr = json.loads(raw)
        if isinstance(arr, list) and arr:
            return [str(s).strip() for s in arr if str(s).strip()]
        return [user_message.strip()]
    except Exception:
        return [user_message.strip()]


# --- Synthesis with sources and Gallica links ---
SYNTHESIS_SYSTEM = """Tu es un assistant qui présente des remèdes historiques à base de plantes, à partir d'extraits d'ouvrages français numérisés (Gallica).

Règles strictes:
- Utilise UNIQUEMENT les informations des extraits fournis. N'invente rien.
- Traite chaque symptôme séparément avec les passages qui lui correspondent.
- À la fin, fais une synthèse combinant les solutions pour tous les symptômes.
- Pour chaque source citée, incluts le lien Gallica exact fourni entre parenthèses, ex: (lien: https://gallica.bnf.fr/...)
- Réponds en français, de façon claire et structurée (paragraphes, listes à puces).
- Rappelle que ces informations sont historiques et ne remplacent pas un avis médical."""

SYNTHESIS_USER = """L'utilisateur décrit ces symptômes ou problèmes: {symptoms}

Extraits par symptôme (chaque bloc correspond à un symptôme):

{excerpts_by_symptom}

Produis une réponse qui:
1. Traite chaque symptôme avec les remèdes trouvés dans les extraits correspondants
2. Inclut les liens Gallica pour chaque source citée
3. Termine par une synthèse combinant les solutions
"""

# --- Synthèse pour une question de suivi (mode d'emploi, préparation, etc.) ---
FOLLOWUP_SYSTEM = """Tu es un assistant conversationnel qui répond à une question de précision sur des remèdes déjà évoqués (les sources détaillées ont été données dans le message précédent).

Règles strictes:
- Réponds DIRECTEMENT à la question (usage, préparation, posologie si elle figure dans les extraits, application, etc.).
- N'invente rien : base-toi UNIQUEMENT sur les extraits fournis.
- Les extraits sont des textes d'ouvrages anciens (OCR). Ne les qualifies jamais de code ou d'interface.
- Ne propose jamais de gabarit vide : réponse utile en texte courant, ou honnêteté si l'info manque.
- INTERDICTION ABSOLUE dans ta réponse : numéro de page, « p. », « page », titre d'ouvrage précis, lien URL, « source : », « voir Gallica », « lien : ». L'utilisateur a déjà les références dans le premier message ; ici tu parles comme en entretien, sans bibliographie.
- Ne répète pas la liste complète des remèdes du premier message sauf une courte mention si indispensable.
- Rappelle en une phrase que ces infos sont historiques et ne remplacent pas un avis médical."""

FOLLOWUP_USER = """Contexte : l'utilisateur cherchait des remèdes pour : {prior_symptoms}

Rappel conversationnel du fil (ne pas recopier ; ne pas en extraire de numéros de page pour ta réponse) :
{prior_summary}

Question ACTUELLE (réponds surtout à celle-ci, sans citer de pages ni de liens) :
{current_question}

Extraits (seule base factuelle ; sans indication de pagination dans ce bloc) :

{excerpts_by_symptom}

Réponds en français, style clair et direct. Si le mode de consommation n'apparaît pas dans les extraits, dis-le simplement."""


def _format_excerpts_with_links(
    symptoms: List[str],
    passages_by_symptom: dict,
    get_url_fn,
) -> str:
    """Format excerpts grouped by symptom, with Gallica URLs."""
    blocks = []
    for symptom in symptoms:
        passages = passages_by_symptom.get(symptom, [])
        if not passages:
            continue
        lines = [f"=== Symptôme: {symptom} ==="]
        for i, (book_id, page, text) in enumerate(passages, 1):
            url = get_url_fn(book_id, page)
            excerpt = (text or "").strip()[:400]
            lines.append(f"[Extrait {i}] {excerpt}{'...' if len((text or '').strip()) > 400 else ''}")
            lines.append(f"Source: {book_id} p.{page} | Lien: {url}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def _format_excerpts_for_followup(
    symptoms: List[str],
    passages_by_symptom: dict,
    max_chars_per_excerpt: int = 450,
) -> str:
    """Excerpts for follow-up prompts: no page numbers or URLs (reduces citation leakage)."""
    blocks = []
    for symptom in symptoms:
        passages = passages_by_symptom.get(symptom, [])
        if not passages:
            continue
        lines = [f"=== Thème lié à la question précédente : {symptom} ==="]
        for i, (_book_id, _page, text) in enumerate(passages, 1):
            excerpt = (text or "").strip()[:max_chars_per_excerpt]
            tail = "..." if len((text or "").strip()) > max_chars_per_excerpt else ""
            lines.append(f"[Fragment texte {i}] {excerpt}{tail}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def _scrub_references_for_followup_context(text: str) -> str:
    """Remove URLs and obvious page refs from prior assistant text used as context."""
    if not text:
        return ""
    t = re.sub(r"https?://[^\s\])>]+", "", text)
    t = re.sub(r"\(lien\s*:\s*[^)]*\)", "", t, flags=re.IGNORECASE)
    t = re.sub(r"lien\s*:\s*https?://[^\s)]+", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\bSource\s*:\s*[^\n]+", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:900]


def _scrub_followup_answer_output(text: str) -> str:
    """Remove URLs, liens et références de page que le modèle pourrait encore produire."""
    if not text:
        return text
    t = re.sub(r"https?://[^\s\])>]+", "", text)
    t = re.sub(r"\(lien\s*:\s*[^)]*\)", "", t, flags=re.IGNORECASE)
    t = re.sub(r",?\s*lien\s*:\s*[^\s.)]+(?:\s[^\s.)]+)*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\bSource\s*:\s*[^\n]+", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\bp\.\s*\d+\b", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\bpage\s+\d+\b", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+\n", "\n", t)
    t = re.sub(r"  +", " ", t)
    t = re.sub(r"\s*,\s*,", ",", t)
    return t.strip()


def _get_api_error_message(exc: Exception) -> str:
    """Convert OpenAI API exception to a user-friendly message."""
    err_str = str(exc).lower()
    if "insufficient_quota" in err_str or "quota" in err_str or "credits" in err_str:
        return "Crédits OpenAI insuffisants ou quota dépassé. Rechargez votre compte sur platform.openai.com"
    if "invalid_api_key" in err_str or "authentication" in err_str or "401" in err_str:
        return "Clé API OpenAI invalide ou expirée. Vérifiez votre clé dans .streamlit/secrets.toml"
    if "rate_limit" in err_str or "429" in err_str:
        return "Limite de requêtes atteinte. Réessayez dans quelques instants."
    if "context_length" in err_str or "token" in err_str:
        return "Requête trop longue. Réessayez avec une question plus courte."
    return f"Erreur API : {exc}"


def synthesize_with_sources(
    symptoms: List[str],
    passages_by_symptom: dict,
    get_url_fn,
    model: str = "gpt-4o-mini",
    api_base: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Synthesize a response from passages grouped by symptom, with Gallica links.

    Returns:
        (response_text, error_message). On success: (text, None). On failure: (None, error_msg).
    """
    api_key = _get_api_key()
    if not api_key:
        return None, "Clé API OpenAI non configurée. Ajoutez OPENAI_API_KEY dans .streamlit/secrets.toml"
    if not symptoms:
        return None, "Aucun symptôme à traiter."

    excerpts_text = _format_excerpts_with_links(symptoms, passages_by_symptom, get_url_fn)
    if not excerpts_text.strip():
        return None, "Aucun extrait à synthétiser."

    user_content = SYNTHESIS_USER.format(
        symptoms=", ".join(symptoms),
        excerpts_by_symptom=excerpts_text,
    )

    try:
        from openai import OpenAI
        kwargs = {"api_key": api_key}
        if api_base:
            kwargs["base_url"] = api_base
        client = OpenAI(**kwargs)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYNTHESIS_SYSTEM},
                {"role": "user", "content": user_content},
            ],
            max_tokens=2048,
            temperature=0.3,
            timeout=60.0,
        )
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content.strip(), None
        return None, "Réponse vide de l'API."
    except Exception as e:
        err_msg = _get_api_error_message(e)
        # Fallback: essayer gpt-3.5-turbo si gpt-4o-mini échoue
        if model == "gpt-4o-mini":
            try:
                kwargs = {"api_key": api_key}
                if api_base:
                    kwargs["base_url"] = api_base
                client = OpenAI(**kwargs)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": SYNTHESIS_SYSTEM},
                        {"role": "user", "content": user_content},
                    ],
                    max_tokens=2048,
                    temperature=0.3,
                    timeout=60.0,
                )
                if response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content.strip(), None
            except Exception:
                pass
        return None, err_msg


def synthesize_followup(
    current_question: str,
    prior_symptoms: List[str],
    prior_summary: str,
    passages_by_symptom: dict,
    get_url_fn,
    model: str = "gpt-4o-mini",
    api_base: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Answer a follow-up question (how to use, prepare, etc.) using excerpts + short prior context.
    """
    api_key = _get_api_key()
    if not api_key:
        return None, "Clé API OpenAI non configurée. Ajoutez OPENAI_API_KEY dans .streamlit/secrets.toml"

    excerpts_text = _format_excerpts_for_followup(
        list(passages_by_symptom.keys()),
        passages_by_symptom,
    )
    if not excerpts_text.strip():
        return None, "Aucun extrait pour répondre à la question de suivi."

    summary = _scrub_references_for_followup_context(prior_summary)
    if not summary:
        summary = "(Pas de rappel utile — réponds à partir des fragments texte et de la question.)"

    user_content = FOLLOWUP_USER.format(
        prior_symptoms=", ".join(prior_symptoms) if prior_symptoms else "symptômes précédents",
        prior_summary=summary,
        current_question=current_question.strip(),
        excerpts_by_symptom=excerpts_text,
    )

    try:
        from openai import OpenAI
        kwargs = {"api_key": api_key}
        if api_base:
            kwargs["base_url"] = api_base
        client = OpenAI(**kwargs)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": FOLLOWUP_SYSTEM},
                {"role": "user", "content": user_content},
            ],
            max_tokens=2048,
            temperature=0.35,
            timeout=60.0,
        )
        if response.choices and response.choices[0].message.content:
            return _scrub_followup_answer_output(response.choices[0].message.content.strip()), None
        return None, "Réponse vide de l'API."
    except Exception as e:
        err_msg = _get_api_error_message(e)
        if model == "gpt-4o-mini":
            try:
                kwargs = {"api_key": api_key}
                if api_base:
                    kwargs["base_url"] = api_base
                client = OpenAI(**kwargs)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": FOLLOWUP_SYSTEM},
                        {"role": "user", "content": user_content},
                    ],
                    max_tokens=2048,
                    temperature=0.35,
                    timeout=60.0,
                )
                if response.choices and response.choices[0].message.content:
                    return _scrub_followup_answer_output(response.choices[0].message.content.strip()), None
            except Exception:
                pass
        return None, err_msg

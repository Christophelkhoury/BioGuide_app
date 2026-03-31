#Projet : BioGuide
#Auteurs : Christophe El Khoury, Tia Kahil, Alaa Hamdan
"""Filtrage des requêtes à risque et messages d'avertissement."""
from typing import List, Tuple


RED_FLAG_KEYWORDS = [
    "douleur thoracique", "poitrine", "cœur", "cardiaque",
    "difficulté respiratoire", "essoufflement", "respiration",
    "saignement abondant", "hémorragie", "sang",
    "perte de conscience", "évanouissement", "syncope",
    "convulsion", "crise", "épilepsie",
    "brûlure grave", "brûlure étendue",
    "empoisonnement", "intoxication", "ingestion",
    "fracture", "traumatisme crânien", "traumatisme",
    "accident vasculaire", "AVC", "accident cérébral",
    "crise cardiaque", "infarctus",
    "urgence", "urgence médicale",
]

# Sensitive keywords that trigger risk notice
RISK_KEYWORDS = [
    "grossesse", "enceinte", "bébé", "nouveau-né", "enfant",
    "allergie", "allergique", "réaction allergique",
    "médicament", "traitement", "dosage", "posologie",
    "contre-indication", "effet secondaire",
]


def check_red_flags(query: str) -> Tuple[bool, List[str]]:
    """Détecte les symptômes d'urgence ; retourne (alerte, mots détectés)."""
    query_lower = query.lower()
    matched = [kw for kw in RED_FLAG_KEYWORDS if kw.lower() in query_lower]
    return len(matched) > 0, matched


def check_risk_keywords(query: str) -> Tuple[bool, List[str]]:
    """Détecte les sujets sensibles ; retourne (risque, mots détectés)."""
    query_lower = query.lower()
    matched = [kw for kw in RISK_KEYWORDS if kw.lower() in query_lower]
    return len(matched) > 0, matched


def get_red_flag_message(matched_keywords: List[str]) -> str:
    """Message d'alerte pour symptômes graves."""
    return (
        "**ATTENTION** : Votre recherche contient des symptômes qui peuvent indiquer "
        "une urgence médicale. Cette application ne peut pas fournir de diagnostic médical. "
        "Consultez immédiatement un professionnel de santé ou appelez les urgences (15 en France)."
    )


def get_risk_notice(matched_keywords: List[str]) -> str:
    """Message d'information pour contexte à risque."""
    return (
        "**Note importante** : Votre recherche concerne des sujets sensibles (grossesse, "
        "allergies, médicaments, etc.). Les informations historiques peuvent ne pas être adaptées "
        "à votre situation. Consultez toujours un professionnel de santé avant toute utilisation."
    )

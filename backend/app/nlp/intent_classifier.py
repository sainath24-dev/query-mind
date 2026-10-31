import re
from typing import Dict, Any, Tuple
from backend.app.nlp.preprocessor import preprocessor


class IntentClassifier:
    def __init__(self):
        pass

    def classify(self, text: str, entities: Dict[str, Any]) -> Tuple[str, float]:
        """
        Classifies query intent into one of the canonical categories:
        COUNT, AVERAGE, TOP_N, COMPARISON, GROUP_BY, MAXIMUM, MINIMUM, FILTER, DETAIL_LOOKUP.
        Returns (intent, confidence_score).
        """
        lower = text.lower().strip()
        norm = preprocessor.normalize(text)

        # 1. COMPARISON
        if re.search(r"\b(compare|comparison|versus|vs|difference between)\b", lower):
            return "COMPARISON", 0.95
        if len(entities.get("departments", [])) >= 2 and re.search(r"\b(and|or)\b", lower):
            return "COMPARISON", 0.90

        # 2. TOP_N / RANKING
        if entities.get("limit") is not None and re.search(r"\b(top|first|highest|best|lowest)\s+\d+\b", norm):
            return "TOP_N", 0.98
        if re.search(r"\b(rank|ranking|leaderboard)\b", lower):
            return "TOP_N", 0.88

        # 3. COUNT
        if re.search(r"\b(how many|count|number of|total number|enrolled in each)\b", lower):
            if re.search(r"\b(each|every|per|by)\b", lower):
                return "GROUP_BY", 0.92
            return "COUNT", 0.95

        # 4. MAXIMUM / HIGHEST
        if re.search(r"\b(highest|maximum|max|most|top)\b", lower):
            return "MAXIMUM", 0.92

        # 5. MINIMUM / LOWEST
        if re.search(r"\b(lowest|minimum|min|least|worst|bottom)\b", lower):
            return "MINIMUM", 0.92

        # 6. AVERAGE
        if re.search(r"\b(average|avg|mean)\b", lower):
            if re.search(r"\b(each|every|per|by)\b", lower):
                return "GROUP_BY", 0.92
            return "AVERAGE", 0.94

        # 7. GROUP_BY / DISTRIBUTION
        if re.search(r"\b(distribution|breakdown|by department|by subject|by semester|in each|for each|per department)\b", lower):
            return "GROUP_BY", 0.90

        # 8. DETAIL_LOOKUP (e.g. searching specific USN or student name)
        if re.search(r"\b1ms\d{2}[a-z]{2,5}\d{3}\b", lower):
            return "DETAIL_LOOKUP", 0.95

        # 9. FILTER (has conditions or department / subject filters)
        if entities.get("conditions") or entities.get("departments") or entities.get("subjects") or entities.get("city"):
            return "FILTER", 0.88

        # Default fallback
        return "FILTER", 0.75


intent_classifier = IntentClassifier()

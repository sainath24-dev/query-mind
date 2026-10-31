import re
from typing import Dict, Any, Optional, Tuple


class QueryContext:
    def __init__(self):
        # Maps session_id -> context dictionary
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def get_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._sessions.get(session_id)

    def update_context(
        self,
        session_id: str,
        question: str,
        sql: str,
        intent: str,
        entities: Dict[str, Any],
        tables: list,
        result_metadata: Dict[str, Any]
    ):
        self._sessions[session_id] = {
            "previous_question": question,
            "previous_sql": sql,
            "previous_intent": intent,
            "entities": entities,
            "relevant_tables": tables,
            "result_metadata": result_metadata
        }

    def resolve_followup(
        self,
        current_question: str,
        current_entities: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Detects if current question is a conversational follow-up to previous query context
        and merges constraints (e.g. 'Only show the top 5', 'Only from 3rd year', 'Show their attendance').
        """
        if not context:
            return current_question, current_entities

        lower = current_question.lower().strip()
        merged_entities = dict(context.get("entities", {}))

        # Check for typical follow-up signals
        is_followup = False

        # Signal 1: "Only show top X", "Just the top 5", "Show 5"
        top_match = re.search(r"\b(?:only|just)?\s*(?:show|give|take)?\s*(?:the)?\s*top\s+(\d+)\b", lower)
        if top_match:
            is_followup = True
            new_limit = int(top_match.group(1))
            merged_entities["limit"] = new_limit

        # Signal 2: "Only from 3rd year", "Just 2nd year", "For 4th year"
        year_match = re.search(r"\b(?:only\s+from|just|for|in)?\s*(\d+)(?:st|nd|rd|th)?\s*year\b", lower)
        if year_match:
            is_followup = True
            merged_entities["year"] = int(year_match.group(1))

        # Signal 3: "Only from AIML", "What about CSE?"
        if current_entities.get("departments") and ("only" in lower or "what about" in lower or "from" in lower):
            is_followup = True
            merged_entities["departments"] = current_entities["departments"]

        # Signal 4: "Show their attendance", "Show their marks"
        if re.search(r"\b(their attendance|their marks|their grades)\b", lower):
            is_followup = True
            if "attendance" in lower:
                merged_entities["primary_entity"] = "attendance"
            elif "marks" in lower or "grades" in lower:
                merged_entities["primary_entity"] = "marks"

        if is_followup:
            # Construct synthesized augmented question for the SQL generation layer
            prev_q = context.get("previous_question", "")
            augmented_question = f"{prev_q} (Refined with: {current_question})"
            return augmented_question, merged_entities

        return current_question, current_entities


Tuple_Merged = tuple[str, Dict[str, Any]]

context_service = QueryContext()

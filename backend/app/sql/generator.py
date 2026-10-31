import re
from typing import Dict, Any, Optional, List
from backend.app.services.schema_service import schema_service
from backend.app.llm.provider import get_llm_provider
from backend.app.sql.semantic_rules import semantic_rule_generator

SYSTEM_PROMPT = """You are an expert PostgreSQL Database Architect and NLP SQL Engineer for QueryMind.
Your task is to generate valid, safe, optimized PostgreSQL SELECT SQL queries strictly based on the provided schema and natural language question.

CRITICAL RULES:
1. ONLY generate SELECT or WITH statements. NEVER generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT, or REVOKE.
2. ONLY use the tables and columns provided in the schema context below. NEVER invent or hallucinate tables or columns.
3. Use explicit, standard ANSI JOIN syntax (e.g. JOIN table ON ...).
4. Always qualify column names with table aliases (e.g. s.usn, d.department_code) to avoid ambiguity.
5. Apply appropriate aggregate functions (COUNT, AVG, SUM, MIN, MAX) and GROUP BY clauses where needed.
6. For questions involving string matching (like subject names), use case-insensitive matching with ILIKE '%...%'.
7. Round numerical averages to 2 decimal places using ROUND(AVG(...), 2).
8. If the query does not have an explicit limit, apply LIMIT 50 to prevent unbounded result sets.
9. Return ONLY the raw SQL statement. Do NOT include markdown code blocks (no ```sql), no explanation, no commentary.
"""


class SQLGenerator:
    def __init__(self):
        self.llm_provider = get_llm_provider()

    async def generate_sql(
        self,
        question: str,
        intent: str,
        entities: Dict[str, Any],
        relevant_tables: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generates PostgreSQL SQL query using LLM if available, with automatic semantic rule synthesizer fallback.
        """
        # 1. First synthesize deterministic semantic SQL as robust baseline
        rule_sql = semantic_rule_generator.generate(question, intent, entities, context)

        # 2. Check if LLM provider is configured and available
        if hasattr(self.llm_provider, "is_configured") and self.llm_provider.is_configured():
            # Format tailored schema prompt containing only relevant tables
            schema_text = schema_service.format_relevant_schema_prompt(relevant_tables)

            context_str = ""
            if context and context.get("previous_question"):
                context_str = (
                    f"\nPREVIOUS QUERY CONTEXT:\n"
                    f"Previous Question: {context['previous_question']}\n"
                    f"Previous SQL: {context.get('previous_sql', '')}\n"
                )

            user_prompt = f"""
{schema_text}
{context_str}
USER QUESTION: {question}
DETECTED INTENT: {intent}
EXTRACTED ENTITIES: {entities}

Generate valid PostgreSQL SQL to answer this question.
Return ONLY raw SQL.
"""
            try:
                llm_sql = await self.llm_provider.generate_sql(user_prompt, SYSTEM_PROMPT)
                if llm_sql and ("select" in llm_sql.lower() or "with" in llm_sql.lower()):
                    return llm_sql.strip()
            except Exception:
                pass # fallback to rule generator

        # If LLM not configured or failed, use the semantic rule generator
        if rule_sql:
            return rule_sql.strip()

        # Ultimate fallback
        return "SELECT s.usn, s.first_name, s.last_name, s.cgpa FROM students s ORDER BY s.cgpa DESC LIMIT 10;"


sql_generator = SQLGenerator()

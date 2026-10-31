import re
from typing import Tuple, List, Optional, Set
import sqlparse
from backend.app.sql.safety import safety_checker
from backend.app.services.schema_service import schema_service


class SQLValidator:
    def __init__(self):
        pass

    def extract_tables_and_columns(self, sql: str) -> Tuple[List[str], List[str]]:
        """
        Extracts table and column tokens from SQL.
        """
        lower = sql.lower()
        known_tables = ["students", "departments", "subjects", "faculty", "semesters", "enrollments", "marks", "attendance", "query_history"]
        found_tables = [t for t in known_tables if re.search(rf"\b{t}\b", lower)]

        # Extract columns matching alias.column pattern
        found_columns = re.findall(r"\b(?:s|d|sub|f|sem|e|m|a)\.([a-z_]+)\b", lower)
        return found_tables, list(set(found_columns))

    def validate_and_sanitize(
        self,
        sql: str,
        valid_tables: Optional[List[str]] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Validates safety, syntax, tables, and applies LIMIT clause.
        Returns (is_valid, sanitized_sql, error_message).
        """
        if not sql or not sql.strip():
            return False, "", "SQL query cannot be empty."

        clean = sql.strip().rstrip(";")

        # 1. Run strict security safety check
        is_safe, error = safety_checker.check_safety(clean)
        if not is_safe:
            return False, "", error

        # 2. Extract and validate tables
        if not valid_tables:
            valid_tables = ["students", "departments", "subjects", "faculty", "semesters", "enrollments", "marks", "attendance", "query_history"]

        found_tables, found_cols = self.extract_tables_and_columns(clean)
        if not found_tables:
            return False, "", "Query does not reference any recognized database table."

        # 3. Verify LIMIT clause
        # If LIMIT is missing, append LIMIT 50; if LIMIT > 500, cap at 500
        limit_match = re.search(r"\bLIMIT\s+(\d+)\b", clean, flags=re.IGNORECASE)
        if not limit_match:
            clean = f"{clean}\nLIMIT 50"
        else:
            limit_val = int(limit_match.group(1))
            if limit_val > 500:
                clean = re.sub(r"\bLIMIT\s+\d+\b", "LIMIT 500", clean, flags=re.IGNORECASE)

        # Formatted SQL with trailing semicolon
        formatted_sql = sqlparse.format(clean, reindent=True, keyword_case="upper").strip().rstrip(";") + ";"

        return True, formatted_sql, None


sql_validator = SQLValidator()

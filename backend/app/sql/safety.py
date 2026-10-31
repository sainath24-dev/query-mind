import re
from typing import Tuple, List, Optional
import sqlparse
from sqlparse.sql import Statement, IdentifierList, Identifier, Where, Comparison
from sqlparse.tokens import Keyword, DML, DDL


DANGEROUS_KEYWORDS = {
    "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE",
    "GRANT", "REVOKE", "EXEC", "EXECUTE", "COPY", "VACUUM", "REINDEX",
    "SHUTDOWN", "KILL", "SLEEP", "PG_SLEEP", "CALL", "DO"
}


class SQLSafetyChecker:
    def __init__(self):
        pass

    def check_safety(self, sql: str) -> Tuple[bool, Optional[str]]:
        """
        Inspects SQL query for safety violations, destructive keywords, and injection risks.
        Returns (is_safe, error_message).
        """
        if not sql or not sql.strip():
            return False, "SQL statement is empty."

        clean_sql = sql.strip().rstrip(";")

        # 1. Reject multiple statements separated by semicolon
        # Using sqlparse to split statements
        parsed_statements = [s for s in sqlparse.parse(sql) if s.get_type() != "UNKNOWN" or str(s).strip()]
        if len(parsed_statements) > 1:
            return False, "Security Violation: Multiple SQL statements in a single request are prohibited."

        # 2. Reject dangerous regex keywords in tokens
        normalized_upper = " " + re.sub(r"[\s,()]+", " ", clean_sql.upper()) + " "
        for danger in DANGEROUS_KEYWORDS:
            if re.search(rf"\b{danger}\b", normalized_upper):
                return False, f"Security Violation: Destructive statement or function '{danger}' is prohibited."

        # 3. Check parsed statement type - MUST be SELECT or WITH
        parsed = sqlparse.parse(clean_sql)
        if not parsed:
            return False, "Unable to parse SQL statement."

        stmt: Statement = parsed[0]
        stmt_type = stmt.get_type()
        if stmt_type not in ["SELECT", "UNKNOWN"]: # UNKNOWN often happens for 'WITH ... SELECT'
            return False, f"Security Violation: Only SELECT/WITH queries are permitted. Detected statement type: {stmt_type}."

        first_token = None
        for tok in stmt.tokens:
            if not tok.is_whitespace and tok.value != "":
                first_token = tok.value.upper()
                break

        if first_token not in ["SELECT", "WITH"]:
            return False, f"Security Violation: Query must begin with SELECT or WITH. Found: '{first_token}'."

        return True, None


safety_checker = SQLSafetyChecker()

import time
from typing import Dict, Any, List
from backend.app.database.connection import execute_query_async
from backend.app.config import settings


class SQLExecutor:
    def __init__(self):
        pass

    async def execute_query(self, sql: str) -> Dict[str, Any]:
        """
        Executes validated SQL query using the read-only PostgreSQL connection.
        Enforces execution timeout and transforms rows into JSON-serializable dictionaries.
        """
        start_time = time.perf_counter()

        try:
            columns, rows = await execute_query_async(
                sql=sql,
                readonly=True,
                timeout_seconds=settings.MAX_EXECUTION_TIME_SECONDS
            )
            execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

            return {
                "success": True,
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
                "execution_time_ms": execution_time_ms,
                "error": None
            }

        except Exception as e:
            execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
            error_str = str(e)
            clean_error = error_str.split("\n")[0]
            if "querymind_readonly" in clean_error or "permission denied" in clean_error.lower():
                clean_error = "Database permission error: Execution blocked by read-only security policy."
            elif "statement timeout" in clean_error.lower() or "canceling statement due to statement timeout" in clean_error.lower():
                clean_error = f"Query timed out: Execution exceeded {settings.MAX_EXECUTION_TIME_SECONDS}s limit."

            return {
                "success": False,
                "columns": [],
                "rows": [],
                "row_count": 0,
                "execution_time_ms": execution_time_ms,
                "error": clean_error
            }


sql_executor = SQLExecutor()

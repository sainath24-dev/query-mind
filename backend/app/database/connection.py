import asyncio
from typing import Dict, Any, List, Optional, Tuple
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from backend.app.config import settings

_admin_pool: Optional[ThreadedConnectionPool] = None
_readonly_pool: Optional[ThreadedConnectionPool] = None


def get_admin_pool() -> ThreadedConnectionPool:
    global _admin_pool
    if _admin_pool is None:
        _admin_pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=20,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            dbname=settings.DB_NAME
        )
    return _admin_pool


def get_readonly_pool() -> ThreadedConnectionPool:
    global _readonly_pool
    if _readonly_pool is None:
        _readonly_pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=20,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.RO_DB_USER,
            password=settings.RO_DB_PASS,
            dbname=settings.DB_NAME
        )
    return _readonly_pool


def _sync_execute(pool: ThreadedConnectionPool, sql: str, params: Optional[Dict[str, Any]] = None, timeout_seconds: float = 5.0) -> Tuple[List[str], List[Dict[str, Any]]]:
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            timeout_ms = int(timeout_seconds * 1000)
            cur.execute(f"SET statement_timeout = '{timeout_ms}ms';")

            if params:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
            if cur.description:
                columns = [desc[0] for desc in cur.description]
                rows = []
                for row in cur.fetchall():
                    row_dict = {}
                    for idx, col_name in enumerate(columns):
                        val = row[idx]
                        if hasattr(val, "isoformat"):
                            val = val.isoformat()
                        elif hasattr(val, "__float__") and not isinstance(val, (int, float, bool)):
                            val = float(val)
                        row_dict[col_name] = val
                    rows.append(row_dict)
                conn.commit()
                return columns, rows
            conn.commit()
            return [], []
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


async def execute_query_async(sql: str, params: Optional[Dict[str, Any]] = None, readonly: bool = True, timeout_seconds: float = 5.0) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Non-blocking async query execution offloaded to connection pool worker thread.
    """
    pool = get_readonly_pool() if readonly else get_admin_pool()
    return await asyncio.to_thread(_sync_execute, pool, sql, params, timeout_seconds)

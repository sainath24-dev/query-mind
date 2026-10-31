import os
from typing import Optional
from dotenv import load_dotenv

# Load .env file with exact path without recursive disk scanning
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ENV_PATH = os.path.join(_BASE_DIR, ".env")
if os.path.exists(_ENV_PATH):
    load_dotenv(_ENV_PATH)


class Settings:
    PROJECT_NAME: str = "QueryMind — Natural Language Database Query Assistant"
    API_V1_STR: str = "/api"

    # PostgreSQL Admin (Read-Write) for internal history & schema introspection
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASS: str = os.getenv("DB_PASS", "")
    DB_NAME: str = os.getenv("DB_NAME", "querymind")

    # PostgreSQL Read-Only User for executing user-generated queries safely
    RO_DB_USER: str = os.getenv("RO_DB_USER", "querymind_readonly")
    RO_DB_PASS: str = os.getenv("RO_DB_PASS", "readonly_secure_pass")

    @property
    def DATABASE_URL(self) -> str:
        auth = f"{self.DB_USER}:{self.DB_PASS}@" if self.DB_PASS else f"{self.DB_USER}@"
        return f"postgresql+asyncpg://{auth}{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def READONLY_DATABASE_URL(self) -> str:
        auth = f"{self.RO_DB_USER}:{self.RO_DB_PASS}@"
        return f"postgresql+asyncpg://{auth}{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        auth = f"{self.DB_USER}:{self.DB_PASS}@" if self.DB_PASS else f"{self.DB_USER}@"
        return f"postgresql://{auth}{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Query Execution Constraints
    MAX_EXECUTION_TIME_SECONDS: float = 5.0
    MAX_RESULT_ROWS: int = 500
    DEFAULT_RESULT_LIMIT: int = 50

    # LLM Settings (OpenAI Compatible)
    LLM_API_KEY: Optional[str] = os.getenv("LLM_API_KEY", "")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    LLM_TIMEOUT_SECONDS: float = 15.0

    PORT: int = int(os.getenv("BACKEND_PORT", "8008"))


settings = Settings()

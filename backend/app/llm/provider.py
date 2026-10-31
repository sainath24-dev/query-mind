from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import httpx
from backend.app.config import settings


class LLMProvider(ABC):
    @abstractmethod
    async def generate_sql(self, prompt: str, system_prompt: str) -> Optional[str]:
        pass

    @abstractmethod
    async def generate_explanation(self, prompt: str) -> Optional[str]:
        pass


class OpenAICompatibleProvider(LLMProvider):
    """
    Generic provider for any OpenAI-compatible API endpoint:
    - Official OpenAI (gpt-4o-mini, gpt-4o)
    - Groq, Together, DeepSeek, Fireworks, OpenRouter
    - Local LLM servers: LM Studio (http://localhost:1234/v1), Ollama (http://localhost:11434/v1), vLLM
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = api_key or settings.LLM_API_KEY
        self.base_url = (base_url or settings.LLM_BASE_URL).rstrip("/")
        self.model = model or settings.LLM_MODEL
        self.timeout = settings.LLM_TIMEOUT_SECONDS

    def is_configured(self) -> bool:
        # If connecting to localhost (LM Studio / Ollama), api_key is optional
        if "localhost" in self.base_url or "127.0.0.1" in self.base_url:
            return True
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    async def _post_chat(self, messages: list, temperature: float = 0.0) -> Optional[str]:
        if not self.is_configured():
            return None

        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 800
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    content = data["choices"][0]["message"]["content"]
                    return content.strip()
                else:
                    return None
        except Exception:
            return None

    async def generate_sql(self, prompt: str, system_prompt: str) -> Optional[str]:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        raw = await self._post_chat(messages, temperature=0.0)
        if not raw:
            return None

        # Clean markdown codeblocks if LLM returned ```sql ... ```
        cleaned = raw.strip()
        if "```" in cleaned:
            parts = cleaned.split("```")
            for part in parts:
                p_strip = part.strip()
                if p_strip.lower().startswith("sql"):
                    cleaned = p_strip[3:].strip()
                    break
                elif p_strip.lower().startswith("select") or p_strip.lower().startswith("with"):
                    cleaned = p_strip
                    break

        # Remove trailing semicolon
        cleaned = cleaned.rstrip(";").strip() + ";"
        return cleaned

    async def generate_explanation(self, prompt: str) -> Optional[str]:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are QueryMind's result explanation engine. "
                    "Provide a concise, 1-2 sentence professional natural language explanation "
                    "of the query result grounded strictly in the provided data. "
                    "Do NOT invent facts, numbers, or conclusions not in the results."
                )
            },
            {"role": "user", "content": prompt}
        ]
        return await self._post_chat(messages, temperature=0.2)


def get_llm_provider() -> LLMProvider:
    return OpenAICompatibleProvider()

import logging
from abc import ABC, abstractmethod
from typing import Optional

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...


class LocalTemplateProvider(LLMProvider):
    def generate(self, prompt: str) -> str:
        return prompt

    @property
    def provider_name(self) -> str:
        return "local-template"


class OpenAIProvider(LLMProvider):
    def __init__(self, model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        self._model = model
        self._api_key = api_key

    def generate(self, prompt: str) -> str:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self._api_key)
            response = client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1024,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            logger.warning("OpenAI call failed: %s", exc)
            return f"[OpenAI unavailable: {exc}]"

    @property
    def provider_name(self) -> str:
        return f"openai/{self._model}"


class GeminiProvider(LLMProvider):
    def __init__(self, model: str = "gemini-2.0-flash", api_key: Optional[str] = None):
        self._model = model
        self._api_key = api_key

    def generate(self, prompt: str) -> str:
        try:
            import google.generativeai as genai
            genai.configure(api_key=self._api_key)
            model = genai.GenerativeModel(self._model)
            response = model.generate_content(prompt)
            return response.text or ""
        except Exception as exc:
            logger.warning("Gemini call failed: %s", exc)
            return f"[Gemini unavailable: {exc}]"

    @property
    def provider_name(self) -> str:
        return f"gemini/{self._model}"


class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        self._model = model
        self._base_url = base_url

    def generate(self, prompt: str) -> str:
        try:
            import httpx
            response = httpx.post(
                f"{self._base_url}/api/generate",
                json={"model": self._model, "prompt": prompt, "stream": False},
                timeout=120,
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as exc:
            logger.warning("Ollama call failed: %s", exc)
            return f"[Ollama unavailable: {exc}]"

    @property
    def provider_name(self) -> str:
        return f"ollama/{self._model}"


def get_llm_provider(
    provider: str = "local-template",
    openai_api_key: Optional[str] = None,
    openai_model: str = "gpt-4o-mini",
    gemini_api_key: Optional[str] = None,
    gemini_model: str = "gemini-2.0-flash",
    ollama_model: str = "llama3",
    ollama_base_url: str = "http://localhost:11434",
) -> LLMProvider:
    if provider == "openai":
        return OpenAIProvider(model=openai_model, api_key=openai_api_key)
    if provider == "gemini":
        return GeminiProvider(model=gemini_model, api_key=gemini_api_key)
    if provider == "ollama":
        return OllamaProvider(model=ollama_model, base_url=ollama_base_url)
    return LocalTemplateProvider()

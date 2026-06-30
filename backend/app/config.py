import os

from pydantic import BaseModel


class Settings(BaseModel):
    llm_provider: str = os.getenv("LLM_PROVIDER", "local-template")

    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Gemini
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # Ollama
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


settings = Settings()

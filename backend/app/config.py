from pydantic import BaseModel


class Settings(BaseModel):
    llm_provider: str = "local-template"


settings = Settings()

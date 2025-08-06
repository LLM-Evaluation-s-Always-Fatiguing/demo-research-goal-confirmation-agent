from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    exa_api_key: str
    groq_api_key: str
    openai_api_key: str

    storage_uri: str = "./tmp/storage.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


settings = Settings()


__all__ = ["settings"]

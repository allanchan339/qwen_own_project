"""Application configuration"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings"""

    # API
    api_version: str = "v1"
    debug: bool = False

    # Graphify
    graphify_output_dir: str = "graphify-out"

    # AI/LLM
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None

    # ChromaDB
    chroma_persist_dir: str = "chroma_db"

    model_config = ConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

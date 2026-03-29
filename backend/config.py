from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All provider switching and feature flags live here.
    Never import os.environ directly — use this object instead.
    """

    # Provider switches
    llm_provider: Literal["openai", "pollinations"] = "openai"
    image_provider: Literal["openai", "pollinations", "gemini"] = "openai"
    spotify_enabled: bool = True

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash-image"

    # Spotify
    spotify_client_id: str = ""
    spotify_client_secret: str = ""

    # Server — comma-separated origins e.g. "http://localhost:5173,https://myapp.com"
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    model_config = {"env_file": ".env"}


settings = Settings()

"""
Centralized application settings (Twelve-Factor App compliant).
Utilizes pydantic-settings for type-safe environment configuration.
"""

from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # type: ignore[misc]
    """Centralized application settings for AIPE Blueprint."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    TITLE: str = "AIPE_Framework API"
    DESCRIPTION: str = "Production AI Engineering Blueprint microservice."
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    HEALTH_STATUS: str = "healthy"
    API_KEY: Optional[SecretStr] = None


settings = Settings()

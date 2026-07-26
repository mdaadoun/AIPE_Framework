import os


class Settings:
    """Centralized application settings (Twelve-Factor App compliant)."""

    TITLE: str = os.getenv("AIPE_API_TITLE", "AIPE_Framework API")
    DESCRIPTION: str = os.getenv(
        "AIPE_API_DESCRIPTION",
        "Production API microservice for AIPE Blueprint.",
    )
    VERSION: str = os.getenv("AIPE_API_VERSION", "0.1.0")
    ENVIRONMENT: str = os.getenv("AIPE_ENV", "development")
    HEALTH_STATUS: str = os.getenv("AIPE_HEALTH_STATUS", "healthy")


settings = Settings()

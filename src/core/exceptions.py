"""
Standardized domain exceptions hierarchy for AIPE Framework.
Provides base exception class and specialized application domain errors.
"""


class AIPEError(Exception):
    """Base exception for all AIPE domain errors."""

    pass


class ConfigurationError(AIPEError):
    """Raised when environment variables or configuration settings are missing or invalid."""

    pass


class ValidationError(AIPEError):
    """Raised when input payload or data validation fails."""

    pass


class LLMClientError(AIPEError):
    """Raised when an external LLM API client fails or times out."""

    pass

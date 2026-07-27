from src.core.exceptions import (
    AIPEError,
    ConfigurationError,
    LLMClientError,
    ValidationError,
)


def test_aipe_exceptions_hierarchy():
    base_err = AIPEError("Base error")
    config_err = ConfigurationError("Config error")
    validation_err = ValidationError("Validation error")
    llm_err = LLMClientError("LLM error")

    assert isinstance(config_err, AIPEError)
    assert isinstance(validation_err, AIPEError)
    assert isinstance(llm_err, AIPEError)

    assert str(base_err) == "Base error"
    assert str(config_err) == "Config error"
    assert str(validation_err) == "Validation error"
    assert str(llm_err) == "LLM error"

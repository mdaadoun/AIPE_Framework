from pathlib import Path

import pytest
import yaml


def test_pre_commit_config_exists() -> None:
    """Verify that configuration file .pre-commit-config.yaml exists and is valid YAML."""
    root_dir = Path(__file__).parent.parent
    config_file = root_dir / ".pre-commit-config.yaml"

    assert config_file.exists(), "File .pre-commit-config.yaml is missing."
    assert config_file.stat().st_size > 0, "File .pre-commit-config.yaml is empty."

    try:
        content = config_file.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        assert "repos" in data, "Key 'repos' is missing from .pre-commit-config.yaml."
    except Exception as e:
        pytest.fail(f"File .pre-commit-config.yaml is not valid YAML: {e}")


def test_secrets_baseline_exists() -> None:
    """Verify that .secrets.baseline file exists."""
    root_dir = Path(__file__).parent.parent
    baseline_file = root_dir / ".secrets.baseline"

    assert baseline_file.exists(), "File .secrets.baseline is missing. Run 'detect-secrets scan > .secrets.baseline'."
    assert baseline_file.stat().st_size > 0, "File .secrets.baseline is empty."

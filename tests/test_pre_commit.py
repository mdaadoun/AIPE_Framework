from pathlib import Path

import pytest
import yaml


def test_pre_commit_config_exists() -> None:
    """Vérifie que le fichier de configuration .pre-commit-config.yaml existe et est valide."""
    root_dir = Path(__file__).parent.parent
    config_file = root_dir / ".pre-commit-config.yaml"

    assert config_file.exists(), "Le fichier .pre-commit-config.yaml est manquant."
    assert (
        config_file.stat().st_size > 0
    ), "Le fichier .pre-commit-config.yaml est vide."

    # Vérification de la syntaxe YAML
    try:
        content = config_file.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        assert (
            "repos" in data
        ), "La clé 'repos' est manquante dans .pre-commit-config.yaml."
    except Exception as e:
        pytest.fail(
            f"Le fichier .pre-commit-config.yaml n'est pas un YAML valide : {e}"
        )


def test_secrets_baseline_exists() -> None:
    """Vérifie que le fichier .secrets.baseline existe."""
    root_dir = Path(__file__).parent.parent
    baseline_file = root_dir / ".secrets.baseline"

    assert baseline_file.exists(), "Le fichier .secrets.baseline est manquant. Exécutez 'detect-secrets scan > .secrets.baseline'."
    assert baseline_file.stat().st_size > 0, "Le fichier .secrets.baseline est vide."

"""Tests de validation des prérequis d'onboarding — Étape 6.2 (Zero-Setup Friction).

Ce module vérifie statiquement que tous les éléments nécessaires à un onboarding
réussi en moins de 5 minutes sont présents et correctement configurés :
    - Le README contient les instructions de démarrage rapide.
    - Le Makefile expose les cibles d'onboarding (`install`, `dev`, `test`).
    - La structure de fichiers du projet est complète et cohérente.
    - Le script de simulation d'onboarding est exécutable.
    - L'API de production démarre et répond correctement.

Ces tests ne réalisent PAS un clonage complet (ce serait trop lent pour une
boucle de CI rapide). Le script `scripts/simulate_onboarding.sh` est dédié
à ce scénario de bout en bout.
"""

import subprocess
from pathlib import Path

from fastapi.testclient import TestClient

from src.main import app

# Chemin absolu vers la racine du projet AIPE_Framework
PROJECT_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# SECTION 1 : Complétude de la documentation d'onboarding (README)
# ==============================================================================


def test_readme_exists_and_not_empty() -> None:
    """Vérifie que le fichier README.md existe et n'est pas vide."""
    readme = PROJECT_DIR / "README.md"
    assert readme.exists(), "Le fichier README.md est manquant à la racine du projet."
    assert readme.stat().st_size > 0, "Le fichier README.md est vide."


def test_readme_contains_quickstart_section() -> None:
    """Vérifie que le README contient une section de démarrage rapide."""
    readme = PROJECT_DIR / "README.md"
    content = readme.read_text(encoding="utf-8")

    assert "Démarrage Rapide" in content or "Quick Start" in content, (
        "Le README doit contenir une section 'Démarrage Rapide' (ou 'Quick Start') "
        "pour guider un nouveau développeur."
    )


def test_readme_documents_make_install() -> None:
    """Vérifie que le README documente la commande `make install`."""
    readme = PROJECT_DIR / "README.md"
    content = readme.read_text(encoding="utf-8")

    assert "make install" in content, (
        "Le README doit documenter la commande 'make install' "
        "comme première étape d'onboarding."
    )


def test_readme_documents_make_dev() -> None:
    """Vérifie que le README mentionne le démarrage du serveur ou du dashboard."""
    readme = PROJECT_DIR / "README.md"
    content = readme.read_text(encoding="utf-8")

    has_dev = "make dev" in content
    has_dashboard = "make dashboard" in content
    assert has_dev or has_dashboard, (
        "Le README doit documenter 'make dev' ou 'make dashboard' "
        "pour le lancement du serveur local."
    )


# ==============================================================================
# SECTION 2 : Complétude du Makefile (cibles d'onboarding)
# ==============================================================================


def test_makefile_exists() -> None:
    """Vérifie que le Makefile existe à la racine du projet."""
    makefile = PROJECT_DIR / "Makefile"
    assert makefile.exists(), "Le Makefile est manquant à la racine du projet."
    assert makefile.stat().st_size > 0, "Le Makefile est vide."


def test_makefile_has_install_target() -> None:
    """Vérifie que le Makefile définit la cible 'install'."""
    makefile = PROJECT_DIR / "Makefile"
    content = makefile.read_text(encoding="utf-8")

    assert "\ninstall:" in content or content.startswith(
        "install:"
    ), "Le Makefile doit définir une cible 'install' pour l'onboarding."


def test_makefile_has_dev_target() -> None:
    """Vérifie que le Makefile définit la cible 'dev'."""
    makefile = PROJECT_DIR / "Makefile"
    content = makefile.read_text(encoding="utf-8")

    assert (
        "\ndev:" in content
    ), "Le Makefile doit définir une cible 'dev' pour le démarrage du serveur."


def test_makefile_has_test_target() -> None:
    """Vérifie que le Makefile définit la cible 'test'."""
    makefile = PROJECT_DIR / "Makefile"
    content = makefile.read_text(encoding="utf-8")

    assert (
        "\ntest:" in content
    ), "Le Makefile doit définir une cible 'test' pour la validation QA."


def test_makefile_has_onboarding_check_target() -> None:
    """Vérifie que le Makefile définit la cible 'onboarding-check'."""
    makefile = PROJECT_DIR / "Makefile"
    content = makefile.read_text(encoding="utf-8")

    assert "onboarding-check" in content, (
        "Le Makefile doit définir une cible 'onboarding-check' "
        "pour la simulation d'onboarding."
    )


# ==============================================================================
# SECTION 3 : Complétude de la structure de fichiers
# ==============================================================================


def test_project_has_pyproject_toml() -> None:
    """Vérifie la présence du fichier de configuration centralisé pyproject.toml."""
    assert (
        PROJECT_DIR / "pyproject.toml"
    ).exists(), "Le fichier pyproject.toml est manquant."


def test_project_has_poetry_lock() -> None:
    """Vérifie la présence du fichier de verrouillage poetry.lock."""
    assert (PROJECT_DIR / "poetry.lock").exists(), (
        "Le fichier poetry.lock est manquant. "
        "Un 'make install' ne pourra pas reproduire un environnement déterministe."
    )


def test_project_has_precommit_config() -> None:
    """Vérifie la présence de la configuration pre-commit."""
    assert (
        PROJECT_DIR / ".pre-commit-config.yaml"
    ).exists(), "Le fichier .pre-commit-config.yaml est manquant."


def test_project_has_gitignore() -> None:
    """Vérifie la présence du .gitignore avec les exclusions essentielles."""
    gitignore = PROJECT_DIR / ".gitignore"
    assert gitignore.exists(), "Le fichier .gitignore est manquant."

    content = gitignore.read_text(encoding="utf-8")
    assert ".venv" in content, ".venv doit être ignoré par Git."
    assert "__pycache__" in content, "__pycache__ doit être ignoré par Git."


def test_project_has_src_package() -> None:
    """Vérifie que le paquet source src/ est initialisé avec un __init__.py."""
    src_dir = PROJECT_DIR / "src"
    assert src_dir.is_dir(), "Le dossier src/ est manquant."
    assert (
        src_dir / "__init__.py"
    ).exists(), (
        "Le fichier src/__init__.py est manquant (paquet Python non initialisé)."
    )


def test_project_has_tests_directory() -> None:
    """Vérifie que le dossier tests/ existe et contient des fichiers de test."""
    tests_dir = PROJECT_DIR / "tests"
    assert tests_dir.is_dir(), "Le dossier tests/ est manquant."

    test_files = list(tests_dir.glob("test_*.py"))
    assert (
        len(test_files) > 0
    ), "Le dossier tests/ ne contient aucun fichier de test (test_*.py)."


# ==============================================================================
# SECTION 4 : Script de simulation d'onboarding
# ==============================================================================


def test_onboarding_script_exists() -> None:
    """Vérifie que le script de simulation d'onboarding est présent."""
    script = PROJECT_DIR / "scripts" / "simulate_onboarding.sh"
    assert script.exists(), "Le script scripts/simulate_onboarding.sh est manquant."


def test_onboarding_script_is_executable() -> None:
    """Vérifie que le script de simulation a le droit d'exécution (chmod +x)."""
    script = PROJECT_DIR / "scripts" / "simulate_onboarding.sh"
    assert script.exists(), "Le script est manquant."

    import os
    import stat

    mode = os.stat(script).st_mode
    assert mode & stat.S_IXUSR, (
        "Le script scripts/simulate_onboarding.sh n'est pas exécutable. "
        "Exécutez : chmod +x scripts/simulate_onboarding.sh"
    )


def test_onboarding_script_has_shebang() -> None:
    """Vérifie que le script commence par un shebang bash correct."""
    script = PROJECT_DIR / "scripts" / "simulate_onboarding.sh"
    content = script.read_text(encoding="utf-8")

    assert content.startswith("#!/usr/bin/env bash") or content.startswith(
        "#!/bin/bash"
    ), "Le script doit commencer par un shebang bash (#!/usr/bin/env bash)."


# ==============================================================================
# SECTION 5 : Validation fonctionnelle de l'API (smoke test)
# ==============================================================================


def test_api_healthcheck_responds() -> None:
    """Vérifie que l'API FastAPI répond sur /health après import direct."""
    client = TestClient(app)
    response = client.get("/health")

    assert (
        response.status_code == 200
    ), f"L'endpoint /health a renvoyé le code {response.status_code} au lieu de 200."


def test_api_healthcheck_contract() -> None:
    """Vérifie que la réponse /health respecte le contrat d'interface attendu."""
    client = TestClient(app)
    response = client.get("/health")
    data = response.json()

    assert "status" in data, "Le champ 'status' est manquant dans la réponse /health."
    assert "version" in data, "Le champ 'version' est manquant dans la réponse /health."
    assert (
        "environment" in data
    ), "Le champ 'environment' est manquant dans la réponse /health."
    assert (
        data["status"] == "healthy"
    ), f"Le status doit être 'healthy', reçu : '{data['status']}'."


# ==============================================================================
# SECTION 6 : Validation de la cible make help (documentation intégrée)
# ==============================================================================


def test_make_help_lists_all_critical_targets() -> None:
    """Vérifie que 'make help' affiche toutes les cibles critiques d'onboarding."""
    result = subprocess.run(
        ["make", "help"],
        cwd=str(PROJECT_DIR),
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, "'make help' a échoué."

    # Toutes les cibles que le README mentionne doivent apparaître dans l'aide
    critical_targets = ["install", "clean", "lint", "test", "dev", "dashboard"]
    for target in critical_targets:
        assert f"make {target}" in result.stdout, (
            f"La cible 'make {target}' n'apparaît pas dans 'make help'. "
            f"Un développeur ne pourra pas la découvrir."
        )

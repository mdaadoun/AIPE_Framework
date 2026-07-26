"""Onboarding prerequisite validation tests — Step 6.2 (Zero-Setup Friction).

Statically verifies that all required onboarding elements (< 5 min)
are present and correctly configured.
"""

import os
import stat
import subprocess
from pathlib import Path

from fastapi.testclient import TestClient

from src.main import app

PROJECT_DIR = Path(__file__).resolve().parent.parent


# SECTION 1: Onboarding Documentation Completeness (README)


def test_readme_exists_and_not_empty() -> None:
    """Verify that README.md exists and is not empty."""
    readme = PROJECT_DIR / "README.md"
    assert readme.exists(), "File README.md is missing from project root."
    assert readme.stat().st_size > 0, "File README.md is empty."


def test_readme_contains_quickstart_section() -> None:
    """Verify that README contains a quickstart section."""
    readme = PROJECT_DIR / "README.md"
    content = readme.read_text(encoding="utf-8")

    assert (
        "Démarrage Rapide" in content
        or "Quick Start" in content
        or "Quickstart" in content
    ), "README must contain a 'Quickstart' section."


def test_readme_documents_make_install() -> None:
    """Verify that README documents the 'make install' command."""
    readme = PROJECT_DIR / "README.md"
    content = readme.read_text(encoding="utf-8")

    assert "make install" in content, "README must document 'make install' command."


def test_readme_documents_make_dev() -> None:
    """Verify that README documents local server or dashboard execution."""
    readme = PROJECT_DIR / "README.md"
    content = readme.read_text(encoding="utf-8")

    has_dev = "make dev" in content
    has_dashboard = "make dashboard" in content
    assert (
        has_dev or has_dashboard
    ), "README must document 'make dev' or 'make dashboard'."


# SECTION 2: Makefile Completeness (Onboarding Targets)


def test_makefile_exists() -> None:
    """Verify that Makefile exists at project root."""
    makefile = PROJECT_DIR / "Makefile"
    assert makefile.exists(), "Makefile is missing from project root."
    assert makefile.stat().st_size > 0, "Makefile is empty."


def test_makefile_has_install_target() -> None:
    """Verify that Makefile defines the 'install' target."""
    makefile = PROJECT_DIR / "Makefile"
    content = makefile.read_text(encoding="utf-8")

    assert "\ninstall:" in content or content.startswith(
        "install:"
    ), "Makefile must define an 'install' target."


def test_makefile_has_dev_target() -> None:
    """Verify that Makefile defines the 'dev' target."""
    makefile = PROJECT_DIR / "Makefile"
    content = makefile.read_text(encoding="utf-8")

    assert "\ndev:" in content, "Makefile must define a 'dev' target."


def test_makefile_has_test_target() -> None:
    """Verify that Makefile defines the 'test' target."""
    makefile = PROJECT_DIR / "Makefile"
    content = makefile.read_text(encoding="utf-8")

    assert "\ntest:" in content, "Makefile must define a 'test' target."


def test_makefile_has_onboarding_check_target() -> None:
    """Verify that Makefile defines the 'onboarding-check' target."""
    makefile = PROJECT_DIR / "Makefile"
    content = makefile.read_text(encoding="utf-8")

    assert (
        "onboarding-check" in content
    ), "Makefile must define 'onboarding-check' target."


# SECTION 3: Project File Structure Completeness


def test_project_has_pyproject_toml() -> None:
    """Verify presence of centralized pyproject.toml configuration file."""
    assert (PROJECT_DIR / "pyproject.toml").exists(), "File pyproject.toml is missing."


def test_project_has_poetry_lock() -> None:
    """Verify presence of poetry.lock lockfile."""
    assert (PROJECT_DIR / "poetry.lock").exists(), "File poetry.lock is missing."


def test_project_has_precommit_config() -> None:
    """Verify presence of pre-commit configuration."""
    assert (
        PROJECT_DIR / ".pre-commit-config.yaml"
    ).exists(), "File .pre-commit-config.yaml is missing."


def test_project_has_gitignore() -> None:
    """Verify presence of .gitignore with essential exclusion rules."""
    gitignore = PROJECT_DIR / ".gitignore"
    assert gitignore.exists(), "File .gitignore is missing."

    content = gitignore.read_text(encoding="utf-8")
    assert ".venv" in content, ".venv must be ignored by Git."
    assert "__pycache__" in content, "__pycache__ must be ignored by Git."


def test_project_has_src_package() -> None:
    """Verify that source package src/ is initialized with __init__.py."""
    src_dir = PROJECT_DIR / "src"
    assert src_dir.is_dir(), "Directory src/ is missing."
    assert (src_dir / "__init__.py").exists(), "File src/__init__.py is missing."


def test_project_has_tests_directory() -> None:
    """Verify that tests/ directory exists and contains test files."""
    tests_dir = PROJECT_DIR / "tests"
    assert tests_dir.is_dir(), "Directory tests/ is missing."

    test_files = list(tests_dir.glob("test_*.py"))
    assert len(test_files) > 0, "Directory tests/ contains no test files."


# SECTION 4: Onboarding Simulation Script


def test_onboarding_script_exists() -> None:
    """Verify presence of onboarding simulation script."""
    script = PROJECT_DIR / "scripts" / "simulate_onboarding.sh"
    assert script.exists(), "Script scripts/simulate_onboarding.sh is missing."


def test_onboarding_script_is_executable() -> None:
    """Verify that onboarding simulation script has execute permission (chmod +x)."""
    script = PROJECT_DIR / "scripts" / "simulate_onboarding.sh"
    assert script.exists(), "Script is missing."

    mode = os.stat(script).st_mode
    assert (
        mode & stat.S_IXUSR
    ), "Script scripts/simulate_onboarding.sh is not executable."


def test_onboarding_script_has_shebang() -> None:
    """Verify that script starts with a valid bash shebang."""
    script = PROJECT_DIR / "scripts" / "simulate_onboarding.sh"
    content = script.read_text(encoding="utf-8")

    assert content.startswith("#!/usr/bin/env bash") or content.startswith(
        "#!/bin/bash"
    ), "Script must start with bash shebang."


# SECTION 5: API Functional Smoke Test


def test_api_healthcheck_responds() -> None:
    """Verify that FastAPI responds on GET /health endpoint."""
    client = TestClient(app)
    response = client.get("/health")

    assert (
        response.status_code == 200
    ), f"/health returned status {response.status_code}."


def test_api_healthcheck_contract() -> None:
    """Verify that GET /health response complies with interface contract."""
    client = TestClient(app)
    response = client.get("/health")
    data = response.json()

    assert "status" in data, "'status' key is missing from /health response."
    assert "version" in data, "'version' key is missing from /health response."
    assert "environment" in data, "'environment' key is missing from /health response."
    assert (
        data["status"] == "healthy"
    ), f"Status must be 'healthy', got '{data['status']}'."


# SECTION 6: Integrated Help Documentation Validation


def test_make_help_lists_all_critical_targets() -> None:
    """Verify that 'make help' lists all critical onboarding targets."""
    result = subprocess.run(
        ["make", "help"],
        cwd=str(PROJECT_DIR),
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, "'make help' failed."

    critical_targets = ["install", "clean", "lint", "test", "dev", "dashboard"]
    for target in critical_targets:
        assert (
            f"make {target}" in result.stdout
        ), f"Target 'make {target}' is missing from 'make help'."

import sys
from pathlib import Path

import pytest


def test_python_version() -> None:
    """Verify that Python version meets requirements (>= 3.10)."""
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 10


def test_poetry_configuration_files_exist() -> None:
    """Verify that Poetry configuration files are present at project root."""
    root_dir = Path(__file__).parent.parent
    pyproject_file = root_dir / "pyproject.toml"
    lock_file = root_dir / "poetry.lock"

    assert pyproject_file.exists(), "File pyproject.toml is missing from project root."
    assert lock_file.exists(), "File poetry.lock is missing. Execute 'poetry lock'."
    assert pyproject_file.stat().st_size > 0, "File pyproject.toml is empty."
    assert lock_file.stat().st_size > 0, "File poetry.lock is empty."


def test_dependencies_are_importable() -> None:
    """Verify key production dependencies declared in pyproject.toml are importable."""
    try:
        import fastapi
        import pydantic
        import uvicorn

        assert fastapi.__version__ is not None
        assert pydantic.__version__ is not None
        assert uvicorn.__version__ is not None
    except ImportError as e:
        pytest.fail(f"Failed to import production dependency: {e}")


def test_dev_dependencies_are_importable() -> None:
    """Verify quality and dev tooling dependencies are installed in local environment."""
    try:
        import mypy  # noqa: F401
        import ruff  # noqa: F401

        assert pytest.__version__ is not None
    except ImportError as e:
        pytest.fail(f"Failed to import development dependency: {e}")


def test_venv_directory_exists() -> None:
    """Verify local virtual environment directory .venv is present at project root."""
    root_dir = Path(__file__).parent.parent
    venv_dir = root_dir / ".venv"
    assert venv_dir.exists(), "Directory .venv is missing at project root."
    assert venv_dir.is_dir(), "Path .venv is not a valid directory."


def test_gitignore_ignores_venv() -> None:
    """Verify .gitignore explicitly excludes the .venv/ directory."""
    root_dir = Path(__file__).parent.parent
    gitignore_file = root_dir / ".gitignore"

    assert gitignore_file.exists(), "File .gitignore is missing."
    content = gitignore_file.read_text(encoding="utf-8")

    assert ".venv" in content, "Exclusion rule for .venv/ is missing from .gitignore."

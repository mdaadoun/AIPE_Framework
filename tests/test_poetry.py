import os
import sys
from pathlib import Path

def test_python_version() -> None:
    """Vérifie que la version de Python est compatible (>= 3.10)."""
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 10


def test_poetry_configuration_files_exist() -> None:
    """Vérifie que les fichiers de configuration de Poetry sont présents à la racine."""
    root_dir = Path(__file__).parent.parent
    pyproject_file = root_dir / "pyproject.toml"
    lock_file = root_dir / "poetry.lock"
    
    assert pyproject_file.exists(), "Le fichier pyproject.toml est absent de la racine."
    assert lock_file.exists(), "Le fichier poetry.lock est absent. Exécutez 'poetry lock'."
    assert pyproject_file.stat().st_size > 0, "Le fichier pyproject.toml est vide."
    assert lock_file.stat().st_size > 0, "Le fichier poetry.lock est vide."


def test_dependencies_are_importable() -> None:
    """Vérifie que les dépendances clés déclarées dans pyproject.toml sont importables dans l'environnement."""
    try:
        import fastapi
        import pydantic
        import uvicorn
        
        # Simple vérification de présence de version
        assert fastapi.__version__ is not None
        assert pydantic.__version__ is not None
        assert uvicorn.__version__ is not None
    except ImportError as e:
        assert False, f"Impossible d'importer une dépendance de production : {e}"


def test_dev_dependencies_are_importable() -> None:
    """Vérifie que les outils de dev et qualité déclarés sont installés dans l'environnement local."""
    try:
        import pytest
        import ruff
        import mypy
        
        assert pytest.__version__ is not None
    except ImportError as e:
        assert False, f"Impossible d'importer une dépendance de développement : {e}"

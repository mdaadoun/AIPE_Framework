import subprocess
from pathlib import Path


def test_make_help() -> None:
    """Vérifie que la commande 'make help' s'exécute avec succès et présente les cibles."""
    project_dir = Path(__file__).parent.parent
    result = subprocess.run(
        ["make", "help"],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        check=True,
    )

    assert "make install" in result.stdout
    assert "make clean" in result.stdout
    assert "make lint" in result.stdout
    assert "make test" in result.stdout
    assert "make dashboard" in result.stdout


def test_make_clean() -> None:
    """Vérifie que la commande 'make clean' purge bien les dossiers de cache temporaires."""
    project_dir = Path(__file__).parent.parent

    # Création temporaire de dossiers imitant les caches pour tester la suppression
    fake_pytest_cache = project_dir / ".pytest_cache"
    fake_mypy_cache = project_dir / ".mypy_cache"

    fake_pytest_cache.mkdir(exist_ok=True)
    fake_mypy_cache.mkdir(exist_ok=True)

    subprocess.run(
        ["make", "clean"],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        check=True,
    )

    # Les dossiers doivent avoir été supprimés
    assert (
        not fake_pytest_cache.exists()
    ), "Le dossier de cache .pytest_cache est toujours présent."
    assert (
        not fake_mypy_cache.exists()
    ), "Le dossier de cache .mypy_cache est toujours présent."


def test_make_lint() -> None:
    """Vérifie que la cible 'make lint' s'exécute sans erreur sur notre base de code propre."""
    project_dir = Path(__file__).parent.parent
    result = subprocess.run(
        ["make", "lint"],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
    )

    # Le code doit être conforme et renvoyer un code de retour 0
    assert (
        result.returncode == 0
    ), f"make lint a échoué avec le code de sortie {result.returncode}. Sortie : {result.stdout}"
    assert "Ruff Linter" in result.stdout or "Ruff" in result.stdout
    assert "Mypy" in result.stdout

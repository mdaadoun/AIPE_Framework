import subprocess
from pathlib import Path


def test_make_help() -> None:
    """Verify that 'make help' executes successfully and displays target rules."""
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
    """Verify that 'make clean' purges temporary cache directories."""
    project_dir = Path(__file__).parent.parent

    # Create temporary mock cache directories
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

    # Assert cache directories are deleted
    assert (
        not fake_pytest_cache.exists()
    ), "Cache directory .pytest_cache is still present."
    assert not fake_mypy_cache.exists(), "Cache directory .mypy_cache is still present."


def test_make_lint() -> None:
    """Verify that 'make lint' executes without errors on clean codebase."""
    project_dir = Path(__file__).parent.parent
    result = subprocess.run(
        ["make", "lint"],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
    )

    # Codebase must be clean and return status code 0
    assert (
        result.returncode == 0
    ), f"make lint failed with exit code {result.returncode}. Output: {result.stdout}"
    assert "Ruff Linter" in result.stdout or "Ruff" in result.stdout
    assert "Mypy" in result.stdout

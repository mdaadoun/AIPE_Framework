import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
VENV_BIN = PROJECT_DIR / ".venv" / "bin"


def get_cmd(tool_name: str) -> list[str]:
    bin_path = VENV_BIN / tool_name
    if bin_path.exists():
        return [str(bin_path)]
    return [sys.executable, "-m", tool_name.replace("-", "_")]


def test_detect_secrets_behavior() -> None:
    """Vérifie que detect-secrets détecte correctement un secret exposé dans un fichier."""
    # Création d'un fichier temporaire sous tests/ pour que detect-secrets l'analyse dans le contexte du repo
    secret_file = Path(__file__).parent / "exposed_secret_temp.py"
    secret_file.write_text('API_KEY = "sk-proj-12345"\n')  # pragma: allowlist secret

    try:
        # Exécution de detect-secrets scan sur ce fichier
        cmd = get_cmd("detect-secrets") + ["scan", str(secret_file)]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )

        # Vérification que le secret est détecté dans la sortie JSON
        assert "exposed_secret_temp.py" in result.stdout
        assert "Secret Keyword" in result.stdout
    finally:
        # Nettoyage du fichier temporaire pour ne pas polluer le dépôt
        if secret_file.exists():
            secret_file.unlink()


def test_ruff_lint_behavior(tmp_path: Path) -> None:
    """Vérifie que Ruff détecte les erreurs d'imports inutilisés ou de style."""
    # Fichier contenant un import inutilisé (Règle F401)
    dirty_file = tmp_path / "dirty_code.py"
    dirty_code = (
        "import os\n"  # Import inutilisé
        "def calcul(x: int) -> int:\n"
        "    return x + 1\n"
    )
    dirty_file.write_text(dirty_code)

    # Exécution de Ruff check
    cmd = get_cmd("ruff") + ["check", str(dirty_file)]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    # Doit détecter l'import inutilisé (F401)
    assert "F401" in result.stdout
    assert result.returncode != 0


def test_mypy_strict_behavior(tmp_path: Path) -> None:
    """Vérifie que Mypy en mode strict rejette le code non annoté."""
    # Fichier avec une signature non annotée
    untyped_file = tmp_path / "untyped_code.py"
    untyped_code = (
        "def saluer(nom):\n"  # Manque d'annotation de type (strict interdit)
        "    return 'Bonjour ' + nom\n"
    )
    untyped_file.write_text(untyped_code)

    # Exécution de Mypy en mode strict
    cmd = get_cmd("mypy") + ["--strict", str(untyped_file)]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    # Mypy doit échouer et signaler le manque d'annotation
    assert result.returncode != 0
    assert "Function is missing a type annotation" in result.stdout

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
    """Verify that detect-secrets detects exposed secrets in source files."""
    # Create temporary test file containing exposed mock secret
    secret_file = Path(__file__).parent / "exposed_secret_temp.py"
    secret_file.write_text('API_KEY = "sk-proj-12345"\n')  # pragma: allowlist secret

    try:
        # Run detect-secrets scan on target file
        cmd = get_cmd("detect-secrets") + ["scan", str(secret_file)]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )

        # Assert secret detection in JSON output
        assert "exposed_secret_temp.py" in result.stdout
        assert "Secret Keyword" in result.stdout
    finally:
        # Clean up temporary test file
        if secret_file.exists():
            secret_file.unlink()


def test_ruff_lint_behavior(tmp_path: Path) -> None:
    """Verify that Ruff detects unused imports and lint violations."""
    # File containing an unused import (rule F401)
    dirty_file = tmp_path / "dirty_code.py"
    dirty_code = (
        "import os\n"  # Unused import
        "def compute(x: int) -> int:\n"
        "    return x + 1\n"
    )
    dirty_file.write_text(dirty_code)

    # Run Ruff check
    cmd = get_cmd("ruff") + ["check", str(dirty_file)]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    # Must detect unused import (F401)
    assert "F401" in result.stdout
    assert result.returncode != 0


def test_mypy_strict_behavior(tmp_path: Path) -> None:
    """Verify that strict Mypy rejects unannotated functions."""
    # File with unannotated signature
    untyped_file = tmp_path / "untyped_code.py"
    untyped_code = (
        "def greet(name):\n"  # Missing type annotations (forbidden in strict mode)
        "    return 'Hello ' + name\n"
    )
    untyped_file.write_text(untyped_code)

    # Run Mypy in strict mode
    cmd = get_cmd("mypy") + ["--strict", str(untyped_file)]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    # Assert Mypy failure on unannotated function signature
    assert result.returncode != 0
    assert "Function is missing a type annotation" in result.stdout

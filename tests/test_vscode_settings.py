"""VSCode IDE Configuration Validation Tests (.vscode/).

Verifies that VSCode development configuration files exist,
are syntax valid, and contain required parameters to align local
development with CI checks (pre-commit hooks + Makefile).

Validated files:
    - .vscode/settings.json  : Auto-formatting on save via Ruff.
    - .vscode/extensions.json : Recommended extensions for team onboarding.
"""

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent


# SECTION 1: File Existence & Syntax Validity


def test_vscode_settings_file_exists() -> None:
    """Verify that .vscode/settings.json exists and is not empty."""
    settings_file = PROJECT_DIR / ".vscode" / "settings.json"

    assert settings_file.exists(), "File .vscode/settings.json is missing."
    assert settings_file.stat().st_size > 0, "File .vscode/settings.json is empty."


def test_vscode_extensions_file_exists() -> None:
    """Verify that .vscode/extensions.json exists and is not empty."""
    extensions_file = PROJECT_DIR / ".vscode" / "extensions.json"

    assert extensions_file.exists(), "File .vscode/extensions.json is missing."
    assert extensions_file.stat().st_size > 0, "File .vscode/extensions.json is empty."


def test_vscode_settings_is_valid_json() -> None:
    """Verify that settings.json is valid JSON (stripping JSONC comments)."""
    settings_file = PROJECT_DIR / ".vscode" / "settings.json"
    content = settings_file.read_text(encoding="utf-8")

    cleaned_lines = []
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("//"):
            continue
        cleaned_lines.append(line)

    cleaned_content = "\n".join(cleaned_lines)

    import re

    cleaned_content = re.sub(
        r'(?<=[,{}\[\]\d"])\s*//.*$', "", cleaned_content, flags=re.MULTILINE
    )

    try:
        data = json.loads(cleaned_content)
        assert isinstance(
            data, dict
        ), "File settings.json must contain a root JSON object."
    except json.JSONDecodeError as e:
        raise AssertionError(
            f"File .vscode/settings.json contains invalid JSON: {e}"
        ) from e


def test_vscode_extensions_is_valid_json() -> None:
    """Verify that extensions.json is valid JSON."""
    extensions_file = PROJECT_DIR / ".vscode" / "extensions.json"
    content = extensions_file.read_text(encoding="utf-8")

    cleaned_lines = [
        line for line in content.splitlines() if not line.lstrip().startswith("//")
    ]
    cleaned_content = "\n".join(cleaned_lines)

    try:
        data = json.loads(cleaned_content)
        assert isinstance(
            data, dict
        ), "File extensions.json must contain a root JSON object."
    except json.JSONDecodeError as e:
        raise AssertionError(
            f"File .vscode/extensions.json contains invalid JSON: {e}"
        ) from e


# SECTION 2: Critical Formatting Settings (settings.json)


def _load_settings() -> dict:
    """Helper loading settings.json and stripping JSONC comments."""
    import re

    settings_file = PROJECT_DIR / ".vscode" / "settings.json"
    content = settings_file.read_text(encoding="utf-8")

    cleaned_lines = [
        line for line in content.splitlines() if not line.lstrip().startswith("//")
    ]
    cleaned_content = "\n".join(cleaned_lines)
    cleaned_content = re.sub(
        r'(?<=[,{}\[\]\d"])\s*//.*$', "", cleaned_content, flags=re.MULTILINE
    )

    return json.loads(cleaned_content)


def test_settings_has_ruff_formatter() -> None:
    """Verify that Ruff is configured as default Python formatter."""
    data = _load_settings()

    python_section = data.get("[python]", {})
    assert (
        python_section.get("editor.defaultFormatter") == "charliermarsh.ruff"
    ), "Default Python formatter must be 'charliermarsh.ruff'."


def test_settings_has_format_on_save() -> None:
    """Verify that format-on-save is enabled."""
    data = _load_settings()

    python_section = data.get("[python]", {})
    assert (
        python_section.get("editor.formatOnSave") is True
    ), "Setting 'editor.formatOnSave' must be true for Python."


def test_settings_has_code_actions_on_save() -> None:
    """Verify that codeActionsOnSave (fixAll + organizeImports) are enabled."""
    data = _load_settings()

    python_section = data.get("[python]", {})
    code_actions = python_section.get("editor.codeActionsOnSave", {})

    assert "source.fixAll" in code_actions, "Action 'source.fixAll' must be configured."
    assert (
        "source.organizeImports" in code_actions
    ), "Action 'source.organizeImports' must be configured."


def test_settings_has_correct_line_length() -> None:
    """Verify line-length alignment between VSCode and pyproject.toml."""
    data = _load_settings()

    ruff_line_length = data.get("ruff.lineLength")

    pyproject_file = PROJECT_DIR / "pyproject.toml"
    pyproject_content = pyproject_file.read_text(encoding="utf-8")

    import re

    match = re.search(r"line-length\s*=\s*(\d+)", pyproject_content)
    assert match is not None, "Failed to find 'line-length' in pyproject.toml."
    pyproject_line_length = int(match.group(1))

    assert (
        ruff_line_length == pyproject_line_length
    ), f"Line length mismatch: settings.json={ruff_line_length}, pyproject.toml={pyproject_line_length}."


def test_settings_has_ruff_lint_enabled() -> None:
    """Verify real-time Ruff linting is enabled in editor settings."""
    data = _load_settings()

    assert (
        data.get("ruff.lint.enable") is True
    ), "Setting 'ruff.lint.enable' must be true."


# SECTION 3: Pre-commit Hook Alignment


def test_settings_final_newline_matches_precommit() -> None:
    """Verify final newline insertion aligns with end-of-file-fixer hook."""
    data = _load_settings()

    assert (
        data.get("files.insertFinalNewline") is True
    ), "Setting 'files.insertFinalNewline' must be true."


def test_settings_trim_whitespace_matches_precommit() -> None:
    """Verify trailing whitespace trimming aligns with trailing-whitespace hook."""
    data = _load_settings()

    assert (
        data.get("files.trimTrailingWhitespace") is True
    ), "Setting 'files.trimTrailingWhitespace' must be true."


# SECTION 4: Recommended Extensions (extensions.json)


def test_extensions_recommends_ruff() -> None:
    """Verify Ruff extension is recommended in extensions.json."""
    extensions_file = PROJECT_DIR / ".vscode" / "extensions.json"
    content = extensions_file.read_text(encoding="utf-8")

    cleaned_lines = [
        line for line in content.splitlines() if not line.lstrip().startswith("//")
    ]
    data = json.loads("\n".join(cleaned_lines))

    recommendations = data.get("recommendations", [])
    assert (
        "charliermarsh.ruff" in recommendations
    ), "Extension 'charliermarsh.ruff' must be recommended in extensions.json."


def test_extensions_recommends_python() -> None:
    """Verify Microsoft Python extension is recommended in extensions.json."""
    extensions_file = PROJECT_DIR / ".vscode" / "extensions.json"
    content = extensions_file.read_text(encoding="utf-8")

    cleaned_lines = [
        line for line in content.splitlines() if not line.lstrip().startswith("//")
    ]
    data = json.loads("\n".join(cleaned_lines))

    recommendations = data.get("recommendations", [])
    assert (
        "ms-python.python" in recommendations
    ), "Extension 'ms-python.python' must be recommended in extensions.json."

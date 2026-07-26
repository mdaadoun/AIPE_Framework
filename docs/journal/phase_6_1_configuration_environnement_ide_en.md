# 📌 Session 6.1: IDE Environment Alignment (.vscode/settings.json)

**Date:** July 25, 2026

This session configures VSCode settings to align editor auto-formatting on save with Ruff and Mypy rules enforced in pre-commit hooks.

---

### 1. 🎓 Concepts Introduced

*   **IDE & CI Alignment:** Ensuring developers see identical linter warnings and format fixes in VSCode as enforced by local pre-commit hooks and CI pipelines.
*   **Format on Save (`editor.formatOnSave`):** Automated code formatting triggered instantly upon saving files.

---

### 2. 🧠 Architecture Decision Records (ADRs)

#### Dilemma: Developer IDE Configuration Management
*   **Option 1: Unmanaged Personal IDE Settings**
    *   *Pros/Cons:* Leads to inconsistent code formatting across team members and avoidable pre-commit hook rejections.
*   **Option 2: Version-Controlled `.vscode/settings.json` (Selected)**
    *   *Why this choice?* Guarantees all developers using VSCode auto-format Python files with Ruff on save.

---

### 3. 🛠️ Implementation & Auto-Documentation

#### Configuration in `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  }
}
```

#### Validation Command:
```bash
poetry run pytest tests/test_vscode_settings.py
```
*Expected Output:* Tests confirm valid JSON syntax and correct interpreter paths.

---

### 4. 📌 Session Summary

1.  **IDE Alignment:** Created `.vscode/settings.json` for automated Ruff formatting on save.
2.  **Frictionless DX:** Eliminated manual formatting steps for VSCode developers.

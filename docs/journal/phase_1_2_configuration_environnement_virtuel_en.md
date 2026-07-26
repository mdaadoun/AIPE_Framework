# 📌 Session 1.2: Local Virtual Environment Configuration (.venv)

**Date:** July 23, 2026

This session focuses on configuring Poetry to create and manage the Python virtual environment directly inside the project root directory (`.venv`). This ensures seamless IDE auto-detection and complete environment isolation.

---

### 1. 🎓 Concepts Introduced

*   **In-Project Virtual Environment (`in-project = true`):** Poetry setting enforcing `.venv` creation within the project root folder rather than central system cache directories (`~/.cache/pypoetry`).
*   **IDE Auto-Discovery:** Mechanism by which code editors (VSCode, PyCharm) automatically detect local interpreter paths (`.venv/bin/python`) without manual user configuration.
*   **Git Exclusion Rule:** Safeguard in `.gitignore` preventing binary virtual environment files and packages from accidentally entering version control.

---

### 2. 🧠 Architecture Decision Records (ADRs)

#### Dilemma: Virtual Environment Location (Global Cache vs In-Project)
*   **Option 1: Global Cache (`~/.cache/pypoetry/virtualenvs`)**
    *   *Pros/Cons:* Keeps project directories clean, but complicates path resolution for local IDEs and Docker bind mounts.
*   **Option 2: In-Project `.venv` Directory (Selected)**
    *   *Why this choice?* Placing `.venv` at project root guarantees instant IDE integration, predictable paths for Makefile scripts, and hermetic container builds.

---

### 3. 🛠️ Implementation & Auto-Documentation

#### Configuration in `poetry.toml`:
```toml
[virtualenvs]
in-project = true
```

#### `.gitignore` Rule:
```text
.venv/
__pycache__/
*.pyc
```

#### Validation Command:
```bash
poetry run python --version
```
*Expected Output:* Confirms execution using `.venv/bin/python`.

---

### 4. 📌 Session Summary

1.  **Local Hermetic Environment:** Configured Poetry `in-project = true` to isolate dependencies inside `.venv`.
2.  **Version Control Protection:** Ignored `.venv/` in `.gitignore` to prevent binary repository bloat.

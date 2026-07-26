# 📌 Session 2.2: Ruff Integration (Linter & Formatter)

**Date:** July 23, 2026

This session replaces multiple legacy Python linters (Flake8, Black, isort, autoflake) with a single Rust-based tool: **Ruff**. It achieves sub-second code linting and formatting across the codebase.

---

### 1. 🎓 Concepts Introduced

*   **Ruff:** High-performance Python linter and formatter written in Rust, delivering 10x-100x speedups over Python-native tools.
*   **Rule Sets (E, F, I, B):** Standardized rule families covering pycodestyle errors (`E`), Pyflakes bug detection (`F`), isort import sorting (`I`), and flake8-bugbear anti-patterns (`B`).
*   **Zero-Config Convergence:** Consolidating linter settings into a single `[tool.ruff]` section in `pyproject.toml`.

---

### 2. 🧠 Architecture Decision Records (ADRs)

#### Dilemma: Linter Selection (Black + Flake8 + isort vs Ruff)
*   **Option 1: Black + Flake8 + isort + autoflake Stack**
    *   *Pros/Cons:* Standard industry legacy setup, but requires 4 separate dependencies, multiple config files, and slow pre-commit execution times (> 5 seconds).
*   **Option 2: Ruff (Selected)**
    *   *Why this choice?* Ruff replaces all four tools, formats code in milliseconds, simplifies `pyproject.toml`, and speeds up local feedback loops.

---

### 3. 🛠️ Implementation & Auto-Documentation

#### Configuration in `pyproject.toml`:
```toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "B"]
ignore = []
```

#### Validation Command:
```bash
poetry run ruff check . && poetry run ruff format --check .
```
*Expected Output:* All checks pass in under 1 second.

---

### 4. 📌 Session Summary

1.  **Unified Tooling:** Replaced legacy linter stack with Rust-powered Ruff.
2.  **Ultra-fast Local Feedback:** Code formatting and linting complete across all files in milliseconds.

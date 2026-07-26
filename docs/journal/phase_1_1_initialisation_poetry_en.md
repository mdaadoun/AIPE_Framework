# 📌 Session 1.1: Poetry Initialization & pyproject.toml Setup

**Date:** July 23, 2026

This session documents the creation of the project's dependency foundation using Poetry. The goal is to establish a deterministic, reproducible, and isolated Python environment separating production packages from development and quality control tooling.

---

### 1. 🎓 Concepts Introduced

*   **Poetry:** Modern Python dependency management and packaging tool that deterministically resolves dependency graphs and locks exact versions in `poetry.lock`.
*   **pyproject.toml (PEP 518):** Unified configuration file replacing legacy setup files (`setup.py`, `requirements.txt`, `setup.cfg`) by centralizing project metadata and build dependencies.
*   **Transitive Dependency Locking:** Mechanism ensuring that indirect sub-dependencies installed alongside direct packages remain locked to exact immutable versions across all environments.

---

### 2. 🧠 Architecture Decision Records (ADRs)

#### Dilemma: Dependency Manager Selection (requirements.txt vs Poetry)
*   **Option 1: Legacy `requirements.txt` file**
    *   *Pros/Cons:* Simple to learn, but lacks automatic environment isolation, fails to separate dev/prod packages cleanly, and suffers from version drift on transitive dependencies.
*   **Option 2: Poetry (Selected)**
    *   *Why this choice?* Poetry ensures total build reproducibility via `poetry.lock`, natively isolates Python execution, and separates `main` dependencies from `dev` groups in `pyproject.toml`.

---

### 3. 🛠️ Implementation & Auto-Documentation

#### Configuration generated in `pyproject.toml`:
```toml
[tool.poetry]
name = "aipe-framework"
version = "0.1.0"
description = "Blueprint AI Product Engineering Framework"
authors = ["Michael <dev@ai-engineering.local>"]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.110.0"
uvicorn = "^0.28.0"
pydantic = "^2.6.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
ruff = "^0.3.0"
mypy = "^1.8.0"
pre-commit = "^3.6.0"
```

#### Validation Command:
```bash
poetry install
```
*Expected Output:* Poetry resolves the dependency tree and creates `poetry.lock`.

---

### 4. 📌 Session Summary

1.  **Centralized Configuration:** Initialized `pyproject.toml` with strict separation between production and development dependencies.
2.  **Deterministic Lockfile:** Generated `poetry.lock` guaranteeing bit-for-bit reproducible installs.

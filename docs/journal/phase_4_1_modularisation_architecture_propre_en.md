# 📌 Session 4.1: Clean Architecture Package Structuring (`src/`)

**Date:** July 24, 2026

This session establishes the production source directory [`src/`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/src/) using Clean Architecture principles to separate core configuration, data schemas, API routes, and entry points.

---

### 1. 🎓 Concepts Introduced

*   **Clean Architecture Separation:** Organizing code into distinct architectural layers (`core/`, `schemas/`, `api/`) to decouple business logic from framework interfaces.
*   **Explicit Package Modules:** Creating `__init__.py` markers across sub-directories to structure clean Python imports.
*   **Centralized Settings Management:** Managing global application settings using `Settings` class patterns reading from environment variables.

---

### 2. 🧠 Architecture Decision Records (ADRs)

#### Dilemma: Code Structure Layout (Flat vs Layered Package Structure)
*   **Option 1: Flat Single Directory Layout**
    *   *Pros/Cons:* Quick to prototype, but quickly becomes unmanageable as models, routes, and services expand.
*   **Option 2: Layered Clean Package Architecture (Selected)**
    *   *Why this choice?* Separating `core/`, `schemas/`, and `api/ routes` ensures codebase scalability and allows isolated unit testing.

---

### 3. 🛠️ Implementation & Auto-Documentation

#### Package Structure created in `src/`:
```text
src/
├── __init__.py
├── main.py
├── core/
│   ├── __init__.py
│   └── config.py
├── schemas/
│   ├── __init__.py
│   └── health.py
└── api/
    ├── __init__.py
    └── routes/
        ├── __init__.py
        └── health.py
```

#### Validation Command:
```bash
poetry run python -c "import src.main; print('Import successful')"
```
*Expected Output:* Confirms clean package import paths without errors.

---

### 4. 📌 Session Summary

1.  **Modular Package Architecture:** Established `src/` hierarchy with clear separation of concerns.
2.  **Centralized Config Layer:** Implemented `src/core/config.py` reading settings cleanly.

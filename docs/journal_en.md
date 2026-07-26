# 📓 Learning Journal: Blueprint AI Product Engineering

This journal documents framing sessions, architecture decisions, and design choices made during framework specification.

---

## 📅 Session 1: Strategic Framing & Architectural Choices (July 23, 2026)

### Session Objective
Define a standardized technical baseline to eliminate technical debt on AI projects.

### Topics Addressed & Technical Dilemmas
1.  **Dependency Manager: requirements.txt vs Poetry**
    *   *requirements.txt:* Simple, but unstable due to un-locked transitive dependencies.
    *   *Poetry:* Steeper initial learning curve, but ensures determinism (`poetry.lock`) and handles packaging and dependency groups natively.
    *   *Decision:* Unanimous choice of **Poetry** for robustness and production reproducibility.
2.  **Linter & Formatter: Ruff vs Historical Tools (Black + Flake8)**
    *   *Observation:* Having 4 separate tools slows down the local pre-commit pipeline and multiplies configuration files.
    *   *Decision:* Integration of **Ruff** exclusively. Rust-based performance and integrated formatter simplify the tech stack.

### Key Decisions (ADRs)
*   Enforce strict static typing with **Mypy** in `src/` to secure API interfaces.
*   Centralize all build tool configurations in a single `pyproject.toml` file.

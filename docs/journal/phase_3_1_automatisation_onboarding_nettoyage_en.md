# 📌 Session 3.1: Developer Onboarding & Cleanup Automation (Makefile)

**Date:** July 24, 2026

This session introduces a POSIX-compliant `Makefile` to provide standardized CLI targets (`make install`, `make clean`) for instant onboarding and system cleanup.

---

### 1. 🎓 Concepts Introduced

*   **Makefile Interface Abstraction:** Hiding tool-specific CLI invocations (Poetry, pre-commit, pytest, ruff) behind simple uniform command targets.
*   **Phony Targets (`.PHONY`):** Declaring Makefile targets that do not produce physical disk files to prevent name collision bugs.
*   **Zero-Setup Friction:** Onboarding goal reducing developer setup time to under 5 minutes using a single command.

---

### 2. 🧠 Architecture Decision Records (ADRs)

#### Dilemma: CLI Alias Mechanism (Shell Scripts vs Makefile)
*   **Option 1: Custom Bash Scripts (`install.sh`, `clean.sh`)**
    *   *Pros/Cons:* Shell scripts vary across Linux, macOS, and WSL environments and clutter root project directory.
*   **Option 2: POSIX Makefile (Selected)**
    *   *Why this choice?* `make` is universally pre-installed on Linux/macOS systems and offers standard entry points (`make install`, `make clean`).

---

### 3. 🛠️ Implementation & Auto-Documentation

#### Targets in `Makefile`:
```makefile
.PHONY: install clean help

install:
	poetry install
	poetry run pre-commit install

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} +
```

#### Validation Command:
```bash
make clean && make install
```
*Expected Output:* Caches are completely purged and Poetry/pre-commit are installed cleanly.

---

### 4. 📌 Session Summary

1.  **Unified Onboarding:** Created `make install` to configure Poetry and Git pre-commit hooks in one step.
2.  **Environment Hygiene:** Added `make clean` target to scrub all temporary Python build caches.

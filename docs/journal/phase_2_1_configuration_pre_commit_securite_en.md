# 📌 Session 2.1: Pre-commit & Passive Security Configuration

**Date:** July 23, 2026

This session establishes automated Git hook gatekeeping using `pre-commit` and `detect-secrets`. The primary objective is to block accidental commits containing private API keys (OpenAI, Gemini) or malformatted files on developer workstations before they ever touch remote repositories.

---

### 1. 🎓 Concepts Introduced

*   **Pre-commit Hooks:** Automated client-side scripts executed during `git commit` to validate code before recording Git history.
*   **detect-secrets:** Static analysis tool specifically designed to scan code diffs for secret key formats, passwords, and API tokens.
*   **Secrets Baseline (`.secrets.baseline`):** Fingerprint file recording known/approved mock secrets to prevent false positives while detecting *new* genuine secrets.

---

### 2. 🧠 Architecture Decision Records (ADRs)

#### Dilemma: Secret Scanning Location (Cloud CI vs Local Pre-commit)
*   **Option 1: Cloud CI Pipeline Verification**
    *   *Pros/Cons:* Easy to set up globally, but secrets pushed to remote branches remain permanently exposed in Git commit history even if PR builds fail.
*   **Option 2: Local Pre-commit Hook (Selected)**
    *   *Why this choice?* Intercepting secrets *before* Git records the local commit prevents credential leakage into history or cloud servers entirely.

---

### 3. 🛠️ Implementation & Auto-Documentation

#### Configuration in `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

#### Validation Command:
```bash
poetry run pre-commit run --all-files
```
*Expected Output:* All pre-commit checks pass clean with exit code 0.

---

### 4. 📌 Session Summary

1.  **Passive Security Barrier:** Integrated `detect-secrets` hook to prevent API key leaks.
2.  **Automated Hygiene:** Added trailing whitespace and YAML syntax fixers to pre-commit workflow.

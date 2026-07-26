# 🚀 AI Product Engineering Blueprint (AIPE_Framework) — Industrial Framework & Productivity

[![Python 3.11](https://img.shields.io/badge/python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Poetry](https://img.shields.io/badge/poetry-1.7+-60A5FA?style=flat-square&logo=poetry&logoColor=white)](https://python-poetry.org/)
[![FastAPI 0.110+](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker Multi-Stage](https://img.shields.io/badge/docker-Multi--Stage-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Ruff](https://img.shields.io/badge/linter-Ruff-009688?style=flat-square)](https://github.com/astral-sh/ruff)
[![Mypy strict](https://img.shields.io/badge/typing-Mypy%20strict-blue?style=flat-square)](https://mypy-lang.org/)

[🇫🇷 Version Française disponible ici](README_fr.md)

**AIPE_Framework** (AI Product Engineering Blueprint) is a standardized industrial and technical foundation designed to accelerate and secure the development of AI-based applications (LLMs, RAG, autonomous agents). It eliminates initial technical debt by enforcing production-grade best practices from day one (pre-commit quality gates, 100% strict typing, non-root hardened containerization).

---

## 🎯 Business Goals & Key Performance Indicators (KPIs)

* **Zero-Setup Friction:** Developer onboarding in under 5 minutes flat via a unified toolchain (`git clone` $\to$ `make install` $\to$ ready to code).
* **Native Code Isolation:** Strict separation between exploratory experimentation (`notebooks/`) and production-ready code (`src/`).
* **Systematic Code Quality:** 100% strict Mypy type annotation coverage in `src/` combined with sub-2-second local linting and formatting powered by Rust-based Ruff.
* **Passive Secret Protection:** Local Git gatekeeping via `detect-secrets` pre-commit hooks to automatically block accidental leakages of private API keys (e.g., OpenAI, Gemini).
* **Hardened Containerization:** Multi-stage Docker build producing an ultra-lightweight runtime container (< 250 MB) running under a non-privileged system user (`appuser` UID 1000).

---

## 📂 Repository Structure

```text
AIPE_Framework/
│
├── README.md                   # English main presentation & Quickstart guide
├── README_fr.md                # French version of the blueprint presentation
│
├── dashboard/                  # Interactive Flask learning & recruiter interview simulator
│   ├── app.py                  # Main Flask application entrypoint
│   └── templates/              # SPA HTML UI (index.html)
│
├── docs/                       # Architectural specifications & technical documentation
    ├── specifications_en.md   # Functional & Technical Requirements Specification (FTRS)
    ├── roadmap_en.md          # Chronological step-by-step 6-phase roadmap
    ├── glossary_en.md         # Technical glossary of key framework concepts
    ├── questions_en.md        # Interactive technical interview FAQ (34 Q&A)
    ├── code_en.md             # Source code architecture reference guide
    └── journal_en.md          # Architecture Decision Records (ADR) & development logbook
```

---

## 🛠️ Main Technical Specifications

| Component | File | Technical Role & Rule |
| :--- | :--- | :--- |
| **Tracking Dashboard** | [`dashboard/app.py`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/dashboard/app.py) | Local Flask server for interactive learning and roadmap tracking. |
| **User Interface** | [`dashboard/templates/index.html`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/dashboard/templates/index.html) | Single Page Application (SPA) with modern glassmorphism aesthetic. |
| **Roadmap Spec** | [`docs/roadmap_en.md`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/docs/roadmap_en.md) | Chronological 6-phase linear specification of the AIPE baseline. |
| **Technical Glossary** | [`docs/glossary_en.md`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/docs/glossary_en.md) | In-depth definitions of DevOps, Quality, and IDE concepts (Ruff, Mypy, Poetry). |
| **Interview FAQ** | [`docs/questions_en.md`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/docs/questions_en.md) | 34 targeted recruiter Q&As covering architecture design choices. |
| **Development Log** | [`docs/journal_en.md`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/docs/journal_en.md) | Architectural decision record (ADR) and learning logbook. |

---

## 🚀 Quickstart Guide

### 1. Initialize project (Onboarding)
Installs all dependencies via Poetry and configures local pre-commit Git hooks.
```bash
make install
```

### 2. Launch Interactive Dashboard
Starts the local Flask tracking dashboard.
```bash
make dashboard
```
Access the interactive dashboard UI at [http://localhost:5001](http://localhost:5001).

### 3. Run Automated Test Suite (64 PASSED)
```bash
make test
```

### 4. Execute Code Quality & Linting (Ruff + Strict Mypy)
```bash
make lint
```

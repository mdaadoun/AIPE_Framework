# 📖 Source Code Reference & Architecture Guide

This document provides a detailed breakdown of every module, class, schema, and route in the `src/` directory.

---

## 🛠️ 1. Application Entry Point: `src/main.py`

- **Purpose:** Primary application entry point initializing the global `FastAPI` instance and attaching modular routers.
- **Key Concepts:**
  - `app = FastAPI(...)`: Instantiates the ASGI web application with metadata loaded from central settings (`TITLE`, `DESCRIPTION`, `VERSION`). Automatically exposes OpenAPI docs at `/docs` (Swagger) and `/redoc`.
  - `app.include_router(health.router)`: Attaches sub-routers to keep the root entry point clean, modular, and extensible for future RAG / Agent routes.

---

## ⚙️ 2. Core Configuration: `src/core/config.py`

- **Purpose:** Centralizes application settings adhering to **Twelve-Factor App** principles (loading configuration from environment variables).
- **Key Components:**
  - `class Settings`: Uses `os.getenv(...)` with fallback defaults for local development. Allows seamless environment overrides (e.g. `AIPE_ENV="production"`) during Docker container deployment or cloud orchestration (Kubernetes, Cloud Run).
  - `TITLE`: API title displayed on Swagger docs (`AIPE_API_TITLE`).
  - `DESCRIPTION`: Detailed API description (`AIPE_API_DESCRIPTION`).
  - `VERSION`: Semantic version string (`AIPE_API_VERSION`).
  - `ENVIRONMENT`: Active runtime stage (`AIPE_ENV`, default: `development`).
  - `HEALTH_STATUS`: Default operational status returned by health probe (`AIPE_HEALTH_STATUS`, default: `healthy`).
  - `settings = Settings()`: Shared global instance.

---

## 🩺 3. API Routes: `src/api/routes/health.py`

- **Purpose:** Exposes operational health surveillance endpoints for container orchestrators (Kubernetes, Cloud Run, ECS) and load balancers.
- **Key Concepts:**
  - `router = APIRouter()`: Creates an isolated router instance for health endpoints.
  - `@router.get("/health", response_model=HealthCheckResponse)`: Asynchronous GET route handler.
  - `async def health_check() -> HealthCheckResponse`: Asynchronous function enabling high concurrency on ASGI servers (Uvicorn) without blocking execution threads. Uses Pydantic `HealthCheckResponse` for 100% strict response validation and serialization.

---

## 📐 4. Schemas & Models: `src/schemas/health.py`

- **Purpose:** Defines data validation, parsing, and OpenAPI documentation schemas for health responses using **Pydantic**.
- **Key Components:**
  - `class HealthCheckResponse(BaseModel)`: Pydantic model enforcing type safety:
    - `status: str`: Service status (e.g., `"healthy"`).
    - `environment: str`: Active runtime environment (e.g., `"development"`).
    - `version: str`: Application version (e.g., `"0.1.0"`).
  - Uses `Field(..., description=..., examples=...)` for automatic Swagger documentation generation and strict runtime type enforcement.

---

## 📦 5. Project Manifest & Environment: `pyproject.toml`

- **Purpose:** Centralized project declaration using Poetry. Defines production dependencies (`fastapi`, `uvicorn`, `pydantic`), QA tooling (`pytest`, `ruff`, `mypy`, `pre-commit`, `detect-secrets`), and strict linter/type-checker configurations.
- **Educational Note:** Moving configuration from scattered files into `pyproject.toml` standardizes Python packaging (PEP 518) and guarantees reproducible builds via `poetry.lock`.

---

## 🛠️ 6. Task Automation: `Makefile`

- **Purpose:** Provides a unified command-line entry point for developer workflows (`make install`, `make lint`, `make test`, `make dev`, `make docker-build`, `make onboarding-check`).
- **Educational Note:** Abstracts tool complexity to achieve **Zero-Setup Friction** onboarding for new developers in under 5 minutes.

---

## 🐳 7. Containerization & Security: `Dockerfile`

- **Purpose:** Production multi-stage Docker build producing an unprivileged, hardened runtime container image (< 250 MB).
- **Key Security & Architecture Patterns:**
  - **Multi-Stage Build (`AS builder` -> `AS runtime`):** Compiles dependencies with heavy build tools in Stage 1, then copies only the `.venv` and `src/` into a pristine Python slim image.
  - **Non-Root Hardening:** Creates system user/group (`appuser:appgroup`, UID 1000) and executes with `USER appuser` to enforce the Principle of Least Privilege.
  - **Health Probe:** Configures native `HEALTHCHECK` with `curl` to monitor HTTP operational status every 15s.

---

## 🔐 8. Quality Gatekeeping: `.pre-commit-config.yaml`

- **Purpose:** Configures local git pre-commit hooks to automatically execute trailing whitespace trimming, YAML validation, secret scanning (`detect-secrets`), and code formatting (`ruff`) before code is committed.

---

## 🚀 9. Onboarding Automation: `scripts/simulate_onboarding.sh`

- **Purpose:** Automated E2E verification script that clones the repository into an isolated temporary folder, executes `make install`, boots the server, and validates the `/health` API contract within a 300-second timer.

---

## 📊 10. Interactive Dashboard Backend: `dashboard/app.py`

- **Purpose:** Flask backend service hosting the interactive project dashboard UI, API documentation viewer, dynamic AST-based unit test runner (`/api/run-tests`), and secure source code browser (`/api/code/file`).

---

## ⚙️ 11. IDE Workspace & Extension Recommendations: `.vscode/`

- **Purpose:** Configures workspace settings (`.vscode/settings.json`) and extension recommendations (`.vscode/extensions.json`).
- **Key Concepts:**
  - **`extensions.json`:** Automatically prompts developers opening the workspace to install `charliermarsh.ruff` (linter/formatter) and `ms-python.python` (interpreter & debugging).
  - **`settings.json`:** Aligns local IDE behavior with CI/CD checks by enabling format-on-save via Ruff (`editor.formatOnSave`: `true`), auto-fixing lint errors and imports on save (`source.fixAll`, `source.organizeImports`), and setting `files.insertFinalNewline` & `files.trimTrailingWhitespace`.

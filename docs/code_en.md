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

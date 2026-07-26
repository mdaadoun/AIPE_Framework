# 📖 Source Code Reference & Architecture Guide (EN / FR)

This document provides a detailed breakdown of every module, class, schema, and route in the `src/` directory.

---

## 🛠️ 1. Application Entry Point: `src/main.py`

### 🇬🇧 English Description
- **Purpose:** Primary application entry point initializing the global `FastAPI` instance and attaching modular routers.
- **Key Concepts:**
  - `app = FastAPI(...)`: Instantiates the ASGI web application with metadata loaded from central settings (`TITLE`, `DESCRIPTION`, `VERSION`). Automatically exposes OpenAPI docs at `/docs` (Swagger) and `/redoc`.
  - `app.include_router(health.router)`: Attaches sub-routers to keep the root entry point clean, modular, and extensible for future RAG / Agent routes.

### 🇫🇷 Description Française
- **Rôle :** Point d'entrée principal initialisant l'instance globale `FastAPI` et connectant les routeurs modulaires.
- **Concepts Clés :**
  - `app = FastAPI(...)` : Instancie l'application web ASGI avec les métadonnées chargées depuis la configuration centralisée (`TITLE`, `DESCRIPTION`, `VERSION`). Génère automatiquement la documentation Swagger sur `/docs` et `/redoc`.
  - `app.include_router(health.router)` : Attache les sous-routeurs afin de maintenir un point d'entrée concis et extensible pour de futurs endpoints (RAG, Agents, LLMs).

---

## ⚙️ 2. Core Configuration: `src/core/config.py`

### 🇬🇧 English Description
- **Purpose:** Centralizes application settings adhering to **Twelve-Factor App** principles (loading configuration from environment variables).
- **Key Components:**
  - `class Settings`: Uses `os.getenv(...)` with fallback defaults for local development. Allows seamless environment overrides (e.g. `AIPE_ENV="production"`) during Docker container deployment or cloud orchestration (Kubernetes, Cloud Run).
  - `TITLE`: API title displayed on Swagger docs (`AIPE_API_TITLE`).
  - `DESCRIPTION`: Detailed API description (`AIPE_API_DESCRIPTION`).
  - `VERSION`: Semantic version string (`AIPE_API_VERSION`).
  - `ENVIRONMENT`: Active runtime stage (`AIPE_ENV`, default: `development`).
  - `HEALTH_STATUS`: Default operational status returned by health probe (`AIPE_HEALTH_STATUS`, default: `healthy`).
  - `settings = Settings()`: Shared global instance.

### 🇫🇷 Description Française
- **Rôle :** Centralise la configuration globale de l'application selon les principes **Twelve-Factor App** (lecture via les variables d'environnement).
- **Composants Clés :**
  - `class Settings` : Utilise `os.getenv(...)` avec valeurs par défaut pour le dev local. Permet l'injection dynamique de variables (`AIPE_ENV="production"`) lors des déploiements conteneurisés sans modifier le code source.
  - `TITLE` : Titre de l'API affiché dans la doc Swagger.
  - `DESCRIPTION` : Description détaillée du service.
  - `VERSION` : Version sémantique applicative.
  - `ENVIRONMENT` : Environnement d'exécution actif (`development`, `staging`, `production`).
  - `HEALTH_STATUS` : Statut opérationnel standard renvoyé par la sonde de santé (`healthy`).
  - `settings = Settings()` : Instance globale partagée.

---

## 🩺 3. API Routes: `src/api/routes/health.py`

### 🇬🇧 English Description
- **Purpose:** Exposes operational health surveillance endpoints for container orchestrators (Kubernetes, Cloud Run, ECS) and load balancers.
- **Key Concepts:**
  - `router = APIRouter()`: Creates a isolated router instance for health endpoints.
  - `@router.get("/health", response_model=HealthCheckResponse)`: Asynchronous GET route handler.
  - `async def health_check() -> HealthCheckResponse`: Asynchronous function enabling high concurrency on ASGI servers (Uvicorn) without blocking execution threads. Uses Pydantic `HealthCheckResponse` for 100% strict response validation and serialization.

### 🇫🇷 Description Française
- **Rôle :** Expose les routes de surveillance et d'observabilité opérationnelle exploitées par les orchestrateurs de conteneurs (Kubernetes, Cloud Run) et la supervision.
- **Concepts Clés :**
  - `router = APIRouter()` : Crée une instance de sous-routeur isolée pour les endpoints de santé.
  - `@router.get("/health", response_model=HealthCheckResponse)` : Déclarateur de route GET asynchrone.
  - `async def health_check() -> HealthCheckResponse` : Fonction asynchrone permettant au serveur ASGI (Uvicorn) de traiter des milliers de requêtes concourantes sans bloquer les threads. Utilise le schéma Pydantic `HealthCheckResponse` pour la validation et la sérialisation stricte.

---

## 📐 4. Schemas & Models: `src/schemas/health.py`

### 🇬🇧 English Description
- **Purpose:** Defines data validation, parsing, and OpenAPI documentation schemas for health responses using **Pydantic**.
- **Key Components:**
  - `class HealthCheckResponse(BaseModel)`: Pydantic model enforcing type safety:
    - `status: str`: Service status (e.g., `"healthy"`).
    - `environment: str`: Active runtime environment (e.g., `"development"`).
    - `version: str`: Application version (e.g., `"0.1.0"`).
  - Uses `Field(..., description=..., examples=...)` for automatic Swagger documentation generation and strict runtime type enforcement.

### 🇫🇷 Description Française
- **Rôle :** Définit le schéma de validation, le parsing et la documentation OpenAPI de la réponse de santé grâce à **Pydantic**.
- **Composants Clés :**
  - `class HealthCheckResponse(BaseModel)` : Modèle Pydantic garantissant la propreté des données :
    - `status: str` : Statut opérationnel du service.
    - `environment: str` : Environnement d'exécution actif.
    - `version: str` : Version applicative actuelle.
  - Utilise `Field(..., description=..., examples=...)` pour la génération automatique de la doc Swagger et le contrôle strict des données au runtime.

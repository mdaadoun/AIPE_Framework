# 📖 Guide d'Architecture & Référence du Code Source

Ce document présente une explication détaillée de chaque module, classe, schéma et route contenus dans le répertoire `src/`.

---

## 🛠️ 1. Point d'Entrée Applicatif : `src/main.py`

- **Rôle :** Point d'entrée principal initialisant l'instance globale `FastAPI` et connectant les routeurs modulaires.
- **Concepts Clés :**
  - `app = FastAPI(...)` : Instancie l'application web ASGI avec les métadonnées chargées depuis la configuration centralisée (`TITLE`, `DESCRIPTION`, `VERSION`). Génère automatiquement la documentation Swagger sur `/docs` et `/redoc`.
  - `app.include_router(health.router)` : Attache les sous-routeurs afin de maintenir un point d'entrée concis et extensible pour de futurs endpoints (RAG, Agents, LLMs).

---

## ⚙️ 2. Configuration Globale Core : `src/core/config.py`

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

## 🩺 3. Routes d'API : `src/api/routes/health.py`

- **Rôle :** Expose les routes de surveillance et d'observabilité opérationnelle exploitées par les orchestrateurs de conteneurs (Kubernetes, Cloud Run) et la supervision.
- **Concepts Clés :**
  - `router = APIRouter()` : Crée une instance de sous-routeur isolée pour les endpoints de santé.
  - `@router.get("/health", response_model=HealthCheckResponse)` : Déclarateur de route GET asynchrone.
  - `async def health_check() -> HealthCheckResponse` : Fonction asynchrone permettant au serveur ASGI (Uvicorn) de traiter des milliers de requêtes concourantes sans bloquer les threads. Utilise le schéma Pydantic `HealthCheckResponse` pour la validation et la sérialisation stricte.

---

## 📐 4. Schémas Pydantic : `src/schemas/health.py`

- **Rôle :** Définit le schéma de validation, le parsing et la documentation OpenAPI de la réponse de santé grâce à **Pydantic**.
- **Composants Clés :**
  - `class HealthCheckResponse(BaseModel)` : Modèle Pydantic garantissant la propreté des données :
    - `status: str` : Statut opérationnel du service.
    - `environment: str` : Environnement d'exécution actif.
    - `version: str` : Version applicative actuelle.
  - Utilise `Field(..., description=..., examples=...)` pour la génération automatique de la doc Swagger et le contrôle strict des données au runtime.

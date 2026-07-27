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

---

## 📦 5. Manifeste & Environnement Projet : `pyproject.toml`

- **Rôle :** Déclaration centralisée du projet via Poetry. Définit les dépendances de production (`fastapi`, `uvicorn`, `pydantic`), l'outillage de qualité (`pytest`, `ruff`, `mypy`, `pre-commit`, `detect-secrets`) et les paramètres des linters.
- **Note Pédagogique :** Centraliser la configuration dans `pyproject.toml` respecte la norme PEP 518 et garantit des builds reproductibles grâce à `poetry.lock`.

---

## 🛠️ 6. Automatisation des Tâches : `Makefile`

- **Rôle :** Offre une interface de commandes unifiée pour les workflows de développement (`make install`, `make lint`, `make test`, `make dev`, `make docker-build`, `make onboarding-check`).
- **Note Pédagogique :** Masque la complexité des outils sous-jacents pour garantir un onboarding **Zero-Setup Friction** en moins de 5 minutes.

---

## 🐳 7. Conteneurisation & Sécurité : `Dockerfile`

- **Rôle :** Image Docker de production multi-stage produisant un conteneur d'exécution non-root ultra-sécurisé et léger (< 250 Mo).
- **Patterns d'Architecture & Sécurité :**
  - **Multi-Stage Build (`AS builder` -> `AS runtime`) :** Compile les dépendances avec les outils lourds dans le stage 1, puis ne copie que `.venv` et `src/` dans une image Python slim vierge.
  - **Hardening Non-Root :** Crée un utilisateur/groupe système (`appuser:appgroup`, UID 1000) et bascule l'exécution via `USER appuser` (Principe du moindre privilège).
  - **Sonde de Santé (Healthcheck) :** Configure la directive native `HEALTHCHECK` avec `curl` pour surveiller l'état de l'API toutes les 15 secondes.

---

## 🔐 8. Contrôle Qualité Pré-Commit : `.pre-commit-config.yaml`

- **Rôle :** Configure les hooks Git pre-commit locaux exécutés automatiquement à chaque commit pour vérifier les espaces, valider le YAML, détecter les secrets (`detect-secrets`) et appliquer le linter (`ruff`).

---

## 🚀 9. Simulation d'Onboarding : `scripts/simulate_onboarding.sh`

- **Rôle :** Script de validation automatisé E2E qui clone le dépôt dans un dossier temporaire isolé, exécute `make install`, démarre le serveur et valide le contrat d'interface `/health` en moins de 300 secondes.

---

## 📊 10. Dashboard Interactif : `dashboard-next/`

- **Rôle :** Application Next.js 16 + React 19 + TypeScript alimentant le dashboard interactif, la feuille de route, le glossaire, le simulateur FAQ d'entretien, le lanceur de tests basé sur l'analyse AST Python (`/api/run-tests`) et le navigateur de code source sécurisé (`/api/code/file`).

---

## ⚙️ 11. Configuration de l'Espace de Travail IDE : `.vscode/`

- **Rôle :** Configure l'espace de travail VSCode (`.vscode/settings.json`) et les recommandations d'extensions (`.vscode/extensions.json`).
- **Concepts Clés :**
  - **`extensions.json` :** Propose automatiquement l'installation des extensions officielles `charliermarsh.ruff` (linter/formateur) et `ms-python.python` dès l'ouverture du projet.
  - **`settings.json` :** Aligne le comportement de l'IDE local sur la CI/CD en activant le formatage automatique à la sauvegarde via Ruff (`editor.formatOnSave`: `true`), la correction automatique des erreurs et imports (`source.fixAll`, `source.organizeImports`) et les règles de nettoyage de fin de ligne.

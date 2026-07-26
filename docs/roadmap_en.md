# 🗺️ Detailed Roadmap: AIPE_Framework

This roadmap outlines the chronological sequence of steps to build the core technical baseline of **AIPE_Framework** (Blueprint AI Product Engineering), including theoretical concepts, progress, and validation criteria for each step.

---

## 📊 Synthetic Overview of Phases

```text
Phase 1: Poetry & Setup ──> Phase 2: Quality & Hooks ──> Phase 3: CLI Interface ──> Phase 4: FastAPI App ──> Phase 5: Docker & Security ──> Phase 6: IDE & Onboarding
      (✅ Completed)              (✅ Completed)              (✅ Completed)              (✅ Completed)              (✅ Completed)              (✅ Completed)
```

---

## Phase 1: Isolation & Dependencies (Poetry & Setup) — ✅ Completed
*Objective: Set up a hermetic and deterministic Python virtual environment.*

### Step 1.1: Poetry Initialization & pyproject.toml — ✅ Completed
*   **Description:** Creating the centralized configuration file [`pyproject.toml`](file:///home/michael/Code/job/projets/AIPE_Framework/pyproject.toml) declaring production dependencies (FastAPI, Uvicorn, Pydantic) and separating development dependencies (pytest, ruff, mypy, pre-commit).
*   **Key Concept:** Deterministic dependency management and semantic version declaration.
*   **Validation Criterion:** The `pyproject.toml` file is valid and running `poetry install` generates a `poetry.lock` file.

### Step 1.2: Local Virtual Environment Configuration — ✅ Completed
*   **Description:** Configure Poetry to enforce virtual environment creation directly at project root in a `.venv` directory. Exclude this directory from version control via `.gitignore`.
*   **Key Concept:** Local hermetic isolation and simplified IDE integration.
*   **Validation Criterion:** A local `.venv` folder is created at project root and ignored by `.gitignore`.

---

## Phase 2: Gatekeeping & Quality Control (Pre-commit & Linter) — ✅ Completed
*Objective: Establish security barriers and static analysis close to Git commits.*

### Step 2.1: Pre-commit Configuration & Security — ✅ Completed
*   **Description:** Initializing [`.pre-commit-config.yaml`](file:///home/michael/Code/job/projets/AIPE_Framework/.pre-commit-config.yaml) integrating basic cleanup hooks and the passive security hook `detect-secrets`.
*   **Key Concept:** Active prevention of secret leaks (OpenAI, Gemini API keys) in code repositories.
*   **Validation Criterion:** Committing a file with `API_KEY = "sk-proj-12345"` <!-- pragma: allowlist secret --> is automatically blocked locally by Git.

### Step 2.2: Ruff Integration — ✅ Completed
*   **Description:** Configure Ruff in [`pyproject.toml`](file:///home/michael/Code/job/projets/AIPE_Framework/pyproject.toml) with standard rule sets (E, F, I, B) and integrate into pre-commit.
*   **Key Concept:** Unified high-speed linting and formatting.
*   **Validation Criterion:** Static analysis and formatting execute across all files in under 2 seconds.

### Step 2.3: Static Analysis with Mypy (strict) — ✅ Completed
*   **Description:** Strict configuration of Mypy in [`pyproject.toml`](file:///home/michael/Code/job/projets/AIPE_Framework/pyproject.toml) connected to pre-commit hook to validate application static typing.
*   **Key Concept:** Robustness and formal data type verification.
*   **Validation Criterion:** Any commit containing un-typed Python code or type inconsistencies in `src/` fails.

---

## Phase 3: Unified Command Line Interface (Makefile) — ✅ Completed
*Objective: Provide a standardized command interface eliminating the need to remember complex scripts.*

### Step 3.1: Automation of Onboarding and Cleanup — ✅ Completed
*   **Description:** Writing target commands `make install` (to initialize Poetry and install pre-commit) and `make clean` (to purge all Python, pytest, and mypy cache files) in the [Makefile](file:///home/michael/Code/job/projets/AIPE_Framework/Makefile).
*   **Key Concept:** Standardizing developer onboarding.
*   **Validation Criterion:** The `make clean` command completely removes caches without errors and `make install` sets up the entire environment from scratch.

### Step 3.2: Integration of Test and Execution Validators — ✅ Completed
*   **Description:** Adding command shortcuts `make lint` (ruff + mypy), `make test` (pytest), and `make dev` (starting the local web server).
*   **Key Concept:** Abstraction of underlying tools behind stable interfaces.
*   **Validation Criterion:** Typing `make lint` or `make test` executes internal tools without requiring manual activation of the virtual environment.

---

## Phase 4: FastAPI Core API & Healthcheck — ✅ Completed
*Objective: Build the minimal production web microservice.*

### Step 4.1: API Initialization & Package Structure — ✅ Completed
*   **Description:** Creating the [`src/`](file:///home/michael/Code/job/projets/AIPE_Framework/src/) folder with a clean [`__init__.py`](file:///home/michael/Code/job/projets/AIPE_Framework/src/__init__.py) file and the entry point [`main.py`](file:///home/michael/Code/job/projets/AIPE_Framework/src/main.py) initializing FastAPI.
*   **Key Concept:** Asynchronous ASGI API server.
*   **Validation Criterion:** The server launches locally via `make dev` on port 8000.

### Step 4.2: Compliant Healthcheck Implementation — ✅ Completed
*   **Description:** Adding `/health` route returning the required JSON schema containing `status`, `environment`, and `version` (0.1.0).
*   **Key Concept:** Interface contract and minimal observability.
*   **Validation Criterion:** A GET request to `http://localhost:8000/health` returns the exact targeted JSON payload.

### Step 4.3: API Unit Test Suite — ✅ Completed
*   **Description:** Creating [`tests/test_main.py`](file:///home/michael/Code/job/projets/AIPE_Framework/tests/test_main.py) using `fastapi.testclient` and validating the health route.
*   **Key Concept:** Automated integration testing.
*   **Validation Criterion:** Running `make test` returns 100% success with full test coverage.

---

## Phase 5: Containerization & Multi-Stage Build (Docker) — ✅ Completed
*Objective: Create an ultra-lightweight and highly secured container image.*

### Step 5.1: Multi-stage Dockerfile with Poetry — ✅ Completed
*   **Description:** Writing the [`Dockerfile`](file:///home/michael/Code/ai-engineering/projets/AIPE_Framework/Dockerfile) consisting of a `builder` stage (installing Poetry and compiling dependencies into an internal `.venv`) and a `runtime` stage (copying only `.venv` and source code).
*   **Key Concept:** Separating compilation tools from final runtime (reducing attack surface).
*   **Validation Criterion:** Image build completes successfully and produces an image under 250 MB.

### Step 5.2: Non-root Security Hardening — ✅ Completed
*   **Description:** Create an unprivileged `appuser` user in the final container and transfer file ownership of application executable files to it.
*   **Key Concept:** Principle of least privilege applied to container execution.
*   **Validation Criterion:** Launching container and inspecting running process confirms the server runs under `appuser` identity (UID 1000) rather than `root`.

### Step 5.3: System Monitoring Probe (Healthcheck) — ✅ Completed
*   **Description:** Adding `HEALTHCHECK` clause in Dockerfile polling local API `/health` every 15 seconds using `curl`.
*   **Key Concept:** Native container healthchecking for orchestration (K8s, ECS, Cloud Run).
*   **Validation Criterion:** `docker ps` command displays status `(healthy)` after container startup.

---

## Phase 6: IDE Integration & Final Validation — ✅ Completed
*Objective: Validate overall developer experience and toolchain.*

### Step 6.1: IDE Environment Configuration — ✅ Completed
*   **Description:** Creating VSCode settings file `.vscode/settings.json` to configure auto-formatting on save using official Ruff formatter.
*   **Key Concept:** Aligning development environment with local CI.
*   **Validation Criterion:** Saving a malformatted Python file in VSCode instantly applies formatting fixes.

### Step 6.2: Onboarding Simulation ("Zero-Setup Friction") — ✅ Completed
*   **Description:** Validating complete deployment procedure starting from a clean clone in a temporary folder.
*   **Key Concept:** Onboarding KPI metric.
*   **Validation Criterion:** An external developer clones the project, runs `make install`, and starts server with `make dev` in under 5 minutes total.

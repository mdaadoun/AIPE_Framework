# 📖 Technical Glossary: Blueprint AI Product Engineering (AIPE)

This glossary defines key software engineering and DevOps concepts applied to the industrialization of AI projects within this framework.

---

## 🛠️ Tooling & Environments

### Poetry
Modern dependency management and packaging tool in Python. Unlike `pip` and `requirements.txt`, **Poetry** deterministically resolves complex dependency trees and locks exact versions in a `poetry.lock` file. This guarantees that all developers and CI servers execute the exact same code.

### Virtual Environment (`.venv`)
Isolated directory containing the Python executable and libraries installed specifically for the project. In this framework, the virtual environment is configured locally at the root (`.venv/`) to simplify detection and integration by IDEs (like VSCode or PyCharm).

### Makefile
Configuration file for the system utility `make` (POSIX standard). It defines standardized command aliases (`make install`, `make test`, `make lint`) to offer a unified interface to developers, facilitating onboarding and continuous integration.

### Phony Targets (`.PHONY`)
Directive in a Makefile specifying that listed targets do not correspond to physical files on disk. This avoids name conflicts if a folder or file with the same name were to be created (for example, a `tests/` directory).

### Zero-Setup Friction
Performance indicator (KPI) measuring the effort required to install a complete development environment. The objective is to allow a newcomer to be fully operational with a single standard command (`make install`) in less than 5 minutes.

---

## 🔍 Quality & Static Analysis

### Ruff
Ultra-fast Python linter and code formatter written in Rust. It efficiently replaces older tools like Flake8, Black, isort, and autoflake. Ruff analyzes code and applies formatting in less than a second, accelerating the local feedback loop.

### Mypy
Static type checker for Python. Although Python is a dynamically typed language, using type annotations validated by Mypy (in strict mode) eliminates an entire class of production errors before the code is even executed (e.g., passing invalid types, manipulating `None` elements).

### Static Type Analysis (Type Hinting - PEP 484)
Explicit annotation of data types for function arguments, variables, and return values. Validated during the build phase (by Mypy), it serves as living documentation and prevents runtime bugs without imposing performance overhead at execution.

### Pre-commit Hooks
Git mechanism allowing scripts to run automatically upon issuing a `git commit` command. If any script fails (malformatted code, type errors, or security flaws), the commit is blocked locally, protecting the shared repository's integrity.

---

## 🔒 Security & DevOps

### detect-secrets
Static analysis tool designed to detect API keys (OpenAI, Gemini), passwords, and hardcoded access tokens in source code. Configured as a pre-commit hook, it instantly intercepts attempts to commit private keys.

### Secrets Baseline (`.secrets.baseline`)
JSON file generated at the repository root containing fingerprints (hashes) of identified and approved test secrets or false positives. This file serves as a reference for `detect-secrets` to only report *new* accidentally added secrets, avoiding pipeline blocks due to existing mocks.

### Docker Multi-Stage Build
Optimization technique for Docker images using multiple `FROM` instructions in a single Dockerfile. It allows building dependencies in a heavy intermediate stage (containing compilers and build tools) and copying only necessary compiled artifacts into a lightweight final runtime image (< 250 MB).

### Non-Root Security Hardening
Security practice forcing application execution inside Docker containers under an unprivileged system user (`appuser`) rather than `root`. In case of application compromise, attackers gain no super-user privileges on the host host system.

### Dockerfile
Text file containing ordered instructions (`FROM`, `COPY`, `RUN`, `CMD`) describing how to assemble a Docker image layer by layer. The Dockerfile serves as the build blueprint for application execution environments.

### Docker Layer & Build Cache
Each instruction in a Dockerfile creates an immutable layer. Docker caches these layers and reuses them if input files remain unchanged. Copying manifest files (`pyproject.toml`, `poetry.lock`) *before* application source code allows reusing dependency installation layers during routine code edits.

### Docker Build Context
Set of files sent to the Docker daemon during `docker build`. Excessive build contexts containing `.venv` or `.git` slow down build transfers and risk leaking sensitive files. `.dockerignore` filters this context.

### .dockerignore
Configuration file acting like `.gitignore` for Docker, excluding unnecessary local files (`.venv`, `.git`, development caches) from the Docker build context.

### COPY --from (Inter-Stage Copying)
Multi-stage build instruction copying selective compiled artifacts (e.g. `.venv`) from intermediate builder stages into final runtime stages without carrying along build toolchains.

### Principle of Least Privilege
Fundamental security principle dictating that applications and processes run with minimum necessary permissions. In Docker contexts, this translates to running container processes under unprivileged system users (`appuser`) instead of `root` (UID 0).

### USER Directive (Dockerfile)
Dockerfile instruction switching execution identity for all subsequent commands (`RUN`, `CMD`, `ENTRYPOINT`), ensuring PID 1 starts with restricted user privileges.

### COPY --chown (Docker Ownership Transfer)
`COPY` option assigning file ownership to specific users and groups during copying in a single atomic layer, avoiding extra `RUN chown` layers.

### Privileged vs Unprivileged Network Ports
Linux network ports below 1024 (e.g. 80, 443) require `root` privileges to bind. Ports above 1024 (e.g. 8000 used by Uvicorn) are unprivileged and accessible to non-root users.

### HEALTHCHECK Directive (Dockerfile)
Dockerfile instruction configuring a native health monitoring probe inside containers, declaring command intervals, timeouts, and failure thresholds.

### Container Health Status (Healthy / Unhealthy / Starting)
Container health state managed dynamically by the Docker daemon based on probe results (`starting`, `healthy`, `unhealthy`).

### `curl -f` Option (Fail Fast HTTP)
`-f` (`--fail`) flag forcing `curl` to return non-zero error exit codes when HTTP servers return 4xx or 5xx status codes.

---

## 🌐 Web Architecture & Microservices

### FastAPI
Modern, high-performance web framework for building APIs in Python based on standard type hints and Pydantic, providing automatic OpenAPI documentation generation.

### ASGI (Asynchronous Server Gateway Interface)
Modern Python web server interface succeeding WSGI, natively handling async/await for high concurrency scenarios (WebSocket connections, streaming LLM responses).

### Pydantic
Data validation library leveraging Python type hints, validating incoming/outgoing API data structures and enforcing strict typing.

### APIRouter
FastAPI component modularizing API endpoints into coherent, isolated files (e.g. `/health`, RAG, AI agents) to prevent cluttering `main.py`.

### Separation of Concerns (SoC)
Software architecture principle dividing code into distinct sections with single responsibilities (`core`, `schemas`, `api/routes`, `main.py`).

### Settings Pattern
Engineering practice centralizing configuration variables and metadata in a single class coupled with environment variables.

### Interface Contract
Rigorous technical specification describing structure, data types, HTTP status codes, and endpoint behavior for microservices.

### Observability
Ability to measure and infer internal system states through external outputs (logs, metrics, health endpoints).

### Healthcheck Probe
Automated periodic test mechanism sending requests to container `/health` endpoints to monitor service availability.

### Integration Testing
Testing methodology validating joint execution of multiple components (API server, middleware, configuration, schemas).

### Code Coverage
Statistical metric measuring percentage of executed code lines during test suite runs (enforced at 100% via `fail_under = 100`).

### TestClient
Starlette test utility executing rapid HTTP integration tests on FastAPI apps in a closed local loop without binding live network ports.

---

## 🖥️ IDE & Developer Experience

### Format-on-Save
Editor feature triggering automated formatting (Ruff) upon file save (`Ctrl+S`), eliminating formatting drift.

### JSONC (JSON with Comments)
JSON format variant permitting comments (`//`, `/* */`), used in VSCode configuration files (`.vscode/settings.json`).

### Code Actions on Save
Advanced VSCode mechanism applying automatic code fixes on save (e.g. removing unused imports, reorganizing imports according to PEP 8).

### Workspace Recommendations (`extensions.json`)
Versioned `.vscode/extensions.json` file recommending essential extensions to team members upon opening workspace.

### IDE / CI Alignment (DX Consistency)
Engineering principle ensuring local development editors apply exact formatting and linting rules enforced in CI pipelines.

---

## 🧪 Validation & Onboarding

### Smoke Test
Minimal validation test verifying system boot and responsiveness without fatal errors (e.g. querying `/health` endpoint).

### Structural Completeness Test
Test suite verifying physical presence and consistency of required project files (`README`, `Makefile`, `pyproject.toml`, `.gitignore`).

### Shell Trap (`trap cleanup EXIT`)
Bash mechanism registering cleanup handlers executed automatically upon script termination, ensuring temporary file cleanup.

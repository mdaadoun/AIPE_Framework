"""Multi-Stage Dockerfile and Docker Configuration Validation Tests.

Verifies existence, structure, and compliance of multi-stage Dockerfile
produced in steps 5.1, 5.2, and 5.3 of the AIPE_Framework blueprint.

Step 5.1: Multi-stage build pattern validation.
Step 5.2: Non-root hardening validation (appuser, UID 1000, --chown).
Step 5.3: System monitoring probe validation (HEALTHCHECK, curl, timing).
"""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent


def test_dockerfile_exists() -> None:
    """Verify that Dockerfile exists at project root and is not empty."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    assert dockerfile.exists(), "Dockerfile is missing at project root."
    assert dockerfile.stat().st_size > 0, "Dockerfile is empty."


def test_dockerfile_has_multi_stage_build() -> None:
    """Verify that Dockerfile contains builder and runtime stages."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert "AS builder" in content, "Dockerfile must contain 'AS builder' stage."
    assert "AS runtime" in content, "Dockerfile must contain 'AS runtime' stage."
    assert (
        "--from=builder" in content
    ), "Dockerfile must copy artifacts using '--from=builder'."


def test_dockerfile_installs_only_production_deps() -> None:
    """Verify builder stage installs production dependencies only via '--only main'."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert (
        "--only main" in content
    ), "Dockerfile must use '--only main' in poetry install."


def test_dockerfile_exposes_port_8000() -> None:
    """Verify Dockerfile exposes default port 8000."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert "EXPOSE 8000" in content, "Dockerfile must include 'EXPOSE 8000'."


def test_dockerfile_uses_uvicorn_cmd() -> None:
    """Verify Dockerfile uses Uvicorn targeting 'src.main:app' as entrypoint CMD."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert "uvicorn" in content, "Dockerfile CMD must reference 'uvicorn'."
    assert "src.main:app" in content, "Dockerfile CMD must target 'src.main:app'."


def test_dockerfile_sets_python_env_vars() -> None:
    """Verify presence of PYTHONDONTWRITEBYTECODE and PYTHONUNBUFFERED environment variables."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert (
        "PYTHONDONTWRITEBYTECODE" in content
    ), "Dockerfile must set PYTHONDONTWRITEBYTECODE."
    assert "PYTHONUNBUFFERED" in content, "Dockerfile must set PYTHONUNBUFFERED."


def test_dockerignore_exists() -> None:
    """Verify presence of .dockerignore to optimize build context."""
    dockerignore = PROJECT_DIR / ".dockerignore"
    assert dockerignore.exists(), "File .dockerignore is missing."


def test_dockerignore_excludes_dev_artifacts() -> None:
    """Verify .dockerignore excludes dev artifacts (.venv, .git, tests/, dashboard/, __pycache__)."""
    dockerignore = PROJECT_DIR / ".dockerignore"
    content = dockerignore.read_text(encoding="utf-8")

    expected_exclusions = [".venv", ".git", "tests/", "dashboard-next/", "__pycache__"]
    for exclusion in expected_exclusions:
        assert exclusion in content, f".dockerignore must exclude '{exclusion}'."


# SECTION: Non-root Security Hardening Tests (Step 5.2)


def test_dockerfile_creates_non_root_user() -> None:
    """Verify creation of non-root appgroup and appuser (UID 1000)."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert (
        "addgroup" in content and "appgroup" in content
    ), "Dockerfile must create 'appgroup'."
    assert (
        "adduser" in content and "appuser" in content
    ), "Dockerfile must create 'appuser'."
    assert "1000" in content, "Dockerfile must assign UID 1000 to appuser."


def test_dockerfile_uses_user_directive() -> None:
    """Verify presence of 'USER appuser' directive in Dockerfile."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert (
        "USER appuser" in content
    ), "Dockerfile must include 'USER appuser' directive."


def test_dockerfile_uses_chown_on_copy() -> None:
    """Verify that COPY instructions use '--chown=appuser:appgroup'."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert (
        "--chown=appuser:appgroup" in content
    ), "COPY instructions must include '--chown=appuser:appgroup'."


def test_dockerfile_user_after_copy() -> None:
    """Verify USER directive is placed after COPY instructions in runtime stage."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    runtime_start = content.find("AS runtime")
    runtime_content = content[runtime_start:]

    last_copy_pos = runtime_content.rfind("COPY --from=builder")
    user_pos = runtime_content.find("USER appuser\n")

    assert (
        last_copy_pos != -1 and user_pos != -1
    ), "Runtime stage must contain COPY and USER directives."
    assert (
        user_pos > last_copy_pos
    ), "'USER appuser' must be placed AFTER 'COPY --from=builder'."


# SECTION: System Monitoring Probe Tests (Step 5.3)


def test_dockerfile_has_healthcheck() -> None:
    """Verify presence and parameters of native HEALTHCHECK instruction."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert "HEALTHCHECK" in content, "Dockerfile must include 'HEALTHCHECK'."
    assert (
        "curl" in content and "/health" in content
    ), "HEALTHCHECK must poll '/health' endpoint via curl."
    assert "--interval=15s" in content, "HEALTHCHECK interval must be 15s."
    assert "--timeout=5s" in content, "HEALTHCHECK timeout must be 5s."
    assert "--start-period=10s" in content, "HEALTHCHECK start-period must be 10s."
    assert "--retries=3" in content, "HEALTHCHECK retries must be 3."


def test_dockerfile_runtime_has_curl() -> None:
    """Verify curl installation in runtime stage for HEALTHCHECK probe."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    runtime_start = content.find("AS runtime")
    assert runtime_start != -1, "Runtime stage not defined."
    runtime_content = content[runtime_start:]

    assert (
        "apt-get" in runtime_content and "curl" in runtime_content
    ), "Runtime stage must install curl."


def test_dockerfile_curl_before_user() -> None:
    """Verify curl installation occurs before switching to unprivileged USER."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    runtime_start = content.find("AS runtime")
    runtime_content = content[runtime_start:]

    curl_install_pos = runtime_content.find("RUN apt-get update")
    user_pos = runtime_content.find("USER appuser\n")

    assert (
        curl_install_pos != -1 and user_pos != -1
    ), "Runtime stage must install curl before switching to USER."
    assert (
        curl_install_pos < user_pos
    ), "curl installation must occur BEFORE 'USER appuser'."

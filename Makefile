# ==============================================================================
# Makefile - Unified Command Interface for AIPE_Framework
# ==============================================================================

.PHONY: install clean lint test dev run dashboard dashboard-next docker-build onboarding-check help

help:
	@echo "======================================================================"
	@echo "                   AIPE_Framework - Available Commands                "
	@echo "======================================================================"
	@echo "  make install      - Onboarding: Install dependencies & git hooks."
	@echo "  make clean        - Maintenance: Purge cache & temporary artifacts."
	@echo "  make lint         - Quality: Run Ruff linter/formatter & strict Mypy."
	@echo "  make test         - QA: Run full pytest test suite."
	@echo "  make dev          - Web Server: Start FastAPI server (reload)."
	@echo "  make run          - Executable: Run python main module with ARGS."
	@echo "  make dashboard    - Interface: Start Flask interactive dashboard."
	@echo "  make dashboard-next - Interface: Start Next.js TypeScript interactive dashboard."
	@echo "  make docker-build - Docker: Build multi-stage image (< 250 MB target)."
	@echo "  make onboarding-check - Simulation: Validate < 5 min zero-setup onboarding."
	@echo "======================================================================"

install:
	poetry install
	poetry run pre-commit install

clean:
	@echo "Cleaning cache directories and temporary files..."
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	@echo "--- [1/3] Static analysis (Ruff) ---"
	poetry run ruff check .
	@echo "--- [2/3] Code formatting check (Ruff Format) ---"
	poetry run ruff format --check .
	@echo "--- [3/3] Strict type check (Mypy) ---"
	poetry run python -m mypy src/

test:
	poetry run python -m pytest

dev:
	poetry run uvicorn src.main:app --reload --port 8000 $(ARGS)

run:
	poetry run python -m src.main $(ARGS)

dashboard:
	poetry run python dashboard/app.py

dashboard-next:
	npm --prefix dashboard-next run dev

docker-build:
	@echo "--- Building production multi-stage Docker image ---"
	docker build -t aipe-framework:latest .
	@echo "--- Final image size ---"
	@docker images aipe-framework:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

onboarding-check:
	@echo "--- Zero-Setup Friction Onboarding Simulation ---"
	bash scripts/simulate_onboarding.sh

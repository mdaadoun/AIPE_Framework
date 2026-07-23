# Makefile pour AIPE_Framework
# Interface de commande unifiée pour l'onboarding, la qualité, les tests et le développement.

.PHONY: install clean lint test dev dashboard help

help:
	@echo "Commandes disponibles :"
	@echo "  make install   - Installe les dépendances (Poetry) et configure les hooks git (pre-commit)"
	@echo "  make clean     - Nettoie les caches de compilation et de tests"
	@echo "  make lint      - Exécute le linter Ruff et le vérificateur de types Mypy"
	@echo "  make test      - Exécute la suite de tests unitaires via pytest"
	@echo "  make dashboard - Démarre le tableau de bord de suivi (Flask) sur le port 5001"
	@echo "  make dev       - Démarre le serveur FastAPI de développement (Phase 4)"

install:
	poetry install
	poetry run pre-commit install

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	poetry run ruff check .
	poetry run ruff format --check .
	poetry run mypy src/

test:
	poetry run pytest

dev:
	poetry run uvicorn src.main:app --reload --port 8000

dashboard:
	poetry run python dashboard/app.py

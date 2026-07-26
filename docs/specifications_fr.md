Voici l'analyse stratégique et le **Cahier des Charges Fonctionnel et Technique (CDCFT)** tirés de votre note de cadrage.

---

## 1. Analyse critique du Projet

Le projet adresse directement la **"dette technique initiale"**, responsable du naufrage de la majorité des PoC (Proof of Concept) en IA.

* **Points forts :** L'approche est pragmatique. L'intégration combinée de **Poetry** (déterminisme), **Ruff/Mypy** (rigueur du code et typage) et **Pre-commit** (sécurité passive) crée un cadre robuste. Séparer l'exploration (`notebooks/`) du code destiné à la production (`src/`) est la condition sine qua non pour éviter d'envoyer du code spaghetti en déploiement.
* **Ajustement recommandé (Ruff vs Black) :** Le tableau de la note mentionne à la fois **Ruff** et **Black**. Sachez que Ruff intègre aujourd'hui son propre formateur (compatible à 99% avec Black). Conserver uniquement Ruff simplifie la chaîne de dépendances et gagne encore en vitesse d'exécution.

---

## 2. Cahier des Charges Fonctionnel et Technique (CDCFT)

### Document de Spécifications — Project Baseline & Tooling

```
Projet : Blueprint AI Product Engineering
Version : 1.0.0
Statut : Validation des Spécifications
```

---

### 1. Objectifs & Exigences Clés

#### 1.1 Objectifs Métier

* **Zero-Setup Friction :** Temps d'onboarding d'un développeur inférieur à 5 minutes (`git clone` -> `make install` -> prêt).
* **Industrialisation Native :** Passer de la phase d'expérimentation au déploiement sans restructurer le code source.
* **Sécurité & Conformité :** Zéro fuite de secrets (API Keys, identifiants) dans le suivi de version.

#### 1.2 Métriques de Performance (KPIs)

* **Couverture de typage statique :** 100% du code dans `src/` validé par Mypy (mode strict).
* **Temps d'exécution des checks :** Linting + Formatting < 2 secondes localement via Ruff.
* **Poids de l'image Docker final :** Minimaliste grâce à un build multi-stage (cible < 250 MB pour le runtime).

---

### 2. Spécifications Fonctionnelles

#### F-01 : Isolation & Gestion des Environnements

* Le système doit bloquer l'installation globale de paquets Python sur la machine hôte.
* Les dépendances de **Développement** (pytest, mypy, ruff) doivent être physiquement séparées des dépendances de **Production** (fastapi, pydantic, httpx).

#### F-02 : Gatekeeping & Contrôle Qualité (Pre-commit)

* À chaque commande `git commit`, le système doit automatiquement intercepter les fichiers modifiés et exécuter :
  1. Le nettoyage des espaces et fins de lignes.
  2. La détection de secrets ou clés d'API (via `detect-secrets`).
  3. Le linting et le formatage automatique du code (`ruff`).
  4. L'analyse statique de type (`mypy`).

* Si une seule vérification échoue, le commit doit être bloqué.

#### F-03 : Interface de Commande Unifiée (CLI Local)

L'interaction avec le projet ne doit pas nécessiter de retenir de longues commandes CLI. Un fichier `Makefile` doit faire office d'interface standard :

* `make install` : Initialise l'environnement virtuel, installe les dépendances et configure les hooks Git.
* `make lint` : Lance l'analyse statique et le formatage.
* `make test` : Exécute la suite de tests automatisés avec rapport de couverture.
* `make dev` : Demarre le serveur de développement local.
* `make clean` : Purge les caches Python (`.pytest_cache`, `__pycache__`, `.mypy_cache`).

#### F-04 : Endpoint de Propreté (Healthcheck)

* L'application doit exposer une fonction ou un endpoint minimal `/health` retournant un payload JSON normé :
  ```json
  {
    "status": "healthy",
    "environment": "development",
    "version": "0.1.0"
  }
  ```

---

### 3. Spécifications Techniques & Configurations

#### 3.1 Déclaration des Dépendances Centralisées (`pyproject.toml`)

Toute la configuration des outils doit résider dans le fichier unique `pyproject.toml` pour éviter la multiplication des fichiers de config (`.flake8`, `pytest.ini`, etc.).

```toml
[tool.poetry]
name = "ai-product-engineer-kit"
version = "0.1.0"
description = "Industrial-grade AI Product Engineering Stack"
authors = ["Your Team <team@domain.com>"]
readme = "README.md"
packages = [{include = "src"}]

[tool.poetry.dependencies]
python = "^3.11"
pydantic = "^2.6"
fastapi = "^0.110"
uvicorn = "^0.28"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-asyncio = "^0.23"
ruff = "^0.3"
mypy = "^1.8"
pre-commit = "^3.6"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.ruff]
target-version = "py311"
line-length = 88
select = ["E", "F", "I", "B"] # Errors, Pyflakes, Isort, Bugbear

[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true
```

#### 3.2 Recette de Conteneurisation Optimisée (`Dockerfile`)

Mise en place d'un build multi-stage pour ne pas embarquer le compilateur et les outils dev dans l'image finale :

```dockerfile
# Stage 1: Build & Dependencies
FROM python:3.11-slim AS builder

WORKDIR /app
RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

# Stage 2: Runtime Minimal
FROM python:3.11-slim AS runtime

WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src

EXPOSE 8000
CMD ["python", "-m", "src.main"]
```

---

### 4. Matrice des Livrables

| Livrable | Emplacement | Critère de Validation |
| --- | --- | --- |
| **Manifeste de dépendances** | `/pyproject.toml` | `poetry lock` génère un fichier valide sans conflit. |
| **Pipeline CI Local** | `/.pre-commit-config.yaml` | Bloque un commit contenant `API_KEY = "sk-proj-12345"`. <!-- pragma: allowlist secret --> |
| **Configuration IDE** | `/.vscode/settings.json` | L'enregistrement d'un fichier déclenche le formatage par Ruff. |
| **Suite de Test Vierge** | `/tests/test_main.py` | `pytest` s'exécute avec un taux de réussite de 100%. |
| **Automation CLI** | `/Makefile` | Toutes les commandes cibles s'exécutent sans erreur sous Linux/macOS/WSL. |

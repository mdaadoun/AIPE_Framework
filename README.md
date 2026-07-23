# 🚀 Blueprint AI Product Engineering (AIPE_Framework) — Cadre Industriel & Productivité

[![Python 3.11](https://img.shields.io/badge/python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Poetry](https://img.shields.io/badge/poetry-1.7+-60A5FA?style=flat-square&logo=poetry&logoColor=white)](https://python-poetry.org/)
[![FastAPI 0.110+](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker Multi-Stage](https://img.shields.io/badge/docker-Multi--Stage-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Ruff](https://img.shields.io/badge/linter-Ruff-009688?style=flat-square)](https://github.com/astral-sh/ruff)
[![Mypy strict](https://img.shields.io/badge/typing-Mypy%20strict-blue?style=flat-square)](https://mypy-lang.org/)

AIPE_Framework (Blueprint AI Product Engineering) est un socle technique et industriel standardisé conçu pour accélérer et sécuriser le développement de projets basés sur l'intelligence artificielle (LLMs, RAG, agents). Il résout les problèmes de dette technique initiale en imposant de bonnes pratiques dès le premier jour (contrôle qualité pré-commit, typage strict, conteneurisation optimisée).

---

## 🎯 Objectifs & KPI Métier

* **Zero-Setup Friction :** Onboarding d'un développeur en moins de 5 minutes grâce à un ensemble d'outils unifiés (`git clone` $\to$ `make install` $\to$ prêt pour coder).
* **Isolation Native :** Séparation étanche entre l'expérimentation (`notebooks/`) et le code prêt pour la production (`src/`).
* **Qualité & Rigueur Système :** Couverture de typage statique Mypy strict à 100% dans `src/` et formatage/linting ultrarapide via Ruff en moins de 2 secondes localement.
* **Sécurité Passive :** Blocage automatique au niveau local de toute fuite de secret (ex: clés d'API OpenAI/Gemini) lors du commit via `detect-secrets`.
* **Conteneurisation Optimisée :** Build d'image Docker multi-stage pour un runtime minimaliste (< 250 MB).

---

## 📂 Structure du Projet

```text
AIPE_Framework/
│
├── README.md                   # Présentation du blueprint et guide de démarrage rapide
├── Makefile                    # Interface de commande unique (install, lint, test, dev, clean)
├── pyproject.toml              # Manifeste de dépendances centralisé (Poetry, Ruff, Mypy)
├── poetry.lock                 # Fichier de verrouillage des dépendances
├── .pre-commit-config.yaml     # Configuration des hooks de contrôle qualité Git
├── Dockerfile                  # Recette de conteneurisation multi-stage optimisée
├── .dockerignore               # Fichiers à exclure du contexte de build Docker
│
├── src/                        # Code source destiné à la production
│   ├── __init__.py
│   └── main.py                 # Serveur de développement FastAPI & Healthcheck
│
├── tests/                      # Suite de tests unitaires et d'intégration
│   ├── __init__.py
│   └── test_main.py            # Tests de l'API FastAPI (/health)
│
├── notebooks/                  # Espace d'exploration IA et prototypage Jupyter
│
└── docs/                       # Spécifications et documentation d'architecture
    ├── cahier_charges.md       # Cahier des charges fonctionnel et technique (CDCFT)
    └── roadmap_details.md      # Feuille de route chronologique par étapes
```

---

## 🛠️ Spécifications techniques principales

| Composant | Fichier | Rôle & Règle métier |
| :--- | :--- | :--- |
| **Gestionnaire de dépendances** | [`pyproject.toml`](file:///home/michael/Code/job/projets/AIPE_Framework/pyproject.toml) | Utilisation exclusive de Poetry. Dépendances de développement séparées du runtime principal. |
| **Pipeline CI Local** | [`.pre-commit-config.yaml`](file:///home/michael/Code/job/projets/AIPE_Framework/.pre-commit-config.yaml) | Intercepte les commits Git pour valider : secret leak, ruff format/lint, et types statiques mypy. |
| **Automation CLI** | [`Makefile`](file:///home/michael/Code/job/projets/AIPE_Framework/Makefile) | Abstraction des scripts Python/Poetry pour standardiser l'onboarding et l'exécution locale. |
| **Endpoint /health** | [`src/main.py`](file:///home/michael/Code/job/projets/AIPE_Framework/src/main.py) | API FastAPI avec route `/health` standardisée renvoyant la version et l'état du microservice. |
| **Conteneurisation** | [`Dockerfile`](file:///home/michael/Code/job/projets/AIPE_Framework/Dockerfile) | Séparation de la phase d'installation (stage builder) et d'exécution (stage runtime) non-root. |

---

## 🚀 Démarrage Rapide

### 1. Installation de l'environnement de développement
Pour installer l'environnement virtuel, les dépendances Poetry et configurer automatiquement les hooks pre-commit localement :
```bash
make install
```

### 2. Lancement des validations qualité (Ruff + Mypy)
```bash
make lint
```

### 3. Exécution de la suite de tests
```bash
make test
```

### 4. Démarrage du serveur de développement FastAPI
```bash
make dev
```
Le serveur sera disponible sur [http://localhost:8000](http://localhost:8000), avec la documentation interactive Swagger accessible sur [http://localhost:8000/docs](http://localhost:8000/docs).
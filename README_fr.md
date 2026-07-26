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
├── README.md                   # English main presentation & Quickstart guide
├── README_fr.md                # Version française de la présentation du blueprint
│
├── dashboard/                  # Tableau de bord Flask de suivi et simulation d'entretien
│   ├── app.py                  # Serveur Flask principal
│   └── templates/              # SPA HTML UI (index.html)
│
├── docs/                       # Spécifications et documentation d'architecture
    ├── specifications_fr.md    # Cahier des charges fonctionnel et technique (CDCFT)
    ├── roadmap_fr.md           # Feuille de route chronologique par étapes
    ├── glossary_fr.md          # Glossaire des concepts techniques clés du framework
    ├── questions_fr.md         # FAQ interactive pour la simulation d'entretien oral
    ├── code_guide_fr.md        # Guide bilingue détaillé d'architecture du code source
    └── journal_fr.md           # Journal de bord d'apprentissage et choix d'architecture
```

---

## 🛠️ Spécifications techniques principales

| Composant | Fichier | Rôle & Règle métier |
| :--- | :--- | :--- |
| **Tableau de Bord** | [`dashboard/app.py`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/dashboard/app.py) | Serveur Flask local de suivi et d'apprentissage. |
| **Interface Utilisateur** | [`dashboard/templates/index.html`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/dashboard/templates/index.html) | Single Page Application (SPA) avec design moderne glassmorphism. |
| **Feuille de Route** | [`docs/roadmap_fr.md`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/docs/roadmap_fr.md) | Feuille de route chronologique et linéaire de la Baseline AIPE. |
| **Glossaire Technique** | [`docs/glossary_fr.md`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/docs/glossary_fr.md) | Définitions approfondies des concepts clés (Ruff, Mypy, Poetry). |
| **FAQ d'Entretien** | [`docs/questions_fr.md`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/docs/questions_fr.md) | Questions/réponses ciblées pour la simulation d'entretien technique. |
| **Journal d'Apprentissage** | [`docs/journal_fr.md`](file:///home/michael/Code/ai-engineering/projets/2_AIPE_Framework/docs/journal_fr.md) | Suivi de bord et analyses de décisions techniques. |

---

## 🚀 Démarrage Rapide

### 1. Initialiser le projet (onboarding)
Installe toutes les dépendances via Poetry et configure physiquement les hooks de commit locaux.
```bash
make install
```

### 2. Démarrer le Dashboard de suivi interactif
Lance le serveur de suivi Flask local.
```bash
make dashboard
```
Le tableau de bord de suivi interactif sera accessible sur [http://localhost:5001](http://localhost:5001).

### 3. Exécuter la suite de tests unitaires & QA
```bash
make test
```

### 4. Lancer l'analyse statique de qualité (Ruff + Mypy)
```bash
make lint
```

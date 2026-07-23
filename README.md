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
│
├── dashboard/                  # Tableau de bord Flask de suivi et simulation d'entretien
│   ├── app.py                  # Serveur Flask principal
│   └── templates/              # SPA HTML UI (index.html)
│
├── docs/                       # Spécifications et documentation d'architecture
    ├── cahier_charges.md       # Cahier des charges fonctionnel et technique (CDCFT)
    ├── roadmap_details.md      # Feuille de route chronologique par étapes
    ├── glossaire.md            # Glossaire des concepts techniques clés du framework
    ├── faq_entretien.md        # FAQ interactive pour la simulation d'entretien oral
    └── journal_apprentissage.md # Journal de bord d'apprentissage et choix d'architecture
```

---

## 🛠️ Spécifications techniques principales

| Composant | Fichier | Rôle & Règle métier |
| :--- | :--- | :--- |
| **Tableau de Bord** | [`dashboard/app.py`](file:///home/michael/Code/job/projets/AIPE_Framework/dashboard/app.py) | Serveur Flask local de suivi et d'apprentissage. |
| **Interface Utilisateur** | [`dashboard/templates/index.html`](file:///home/michael/Code/job/projets/AIPE_Framework/dashboard/templates/index.html) | Single Page Application (SPA) avec design moderne glassmorphism. |
| **Feuille de Route** | [`docs/roadmap_details.md`](file:///home/michael/Code/job/projets/AIPE_Framework/docs/roadmap_details.md) | Feuille de route chronologique et linéaire de la Baseline AIPE. |
| **Glossaire Technique** | [`docs/glossaire.md`](file:///home/michael/Code/job/projets/AIPE_Framework/docs/glossaire.md) | Définitions approfondies des concepts clés (Ruff, Mypy, Poetry). |
| **FAQ d'Entretien** | [`docs/faq_entretien.md`](file:///home/michael/Code/job/projets/AIPE_Framework/docs/faq_entretien.md) | Questions/réponses ciblées pour la simulation d'entretien technique. |
| **Journal d'Apprentissage** | [`docs/journal_apprentissage.md`](file:///home/michael/Code/job/projets/AIPE_Framework/docs/journal_apprentissage.md) | Suivi de bord et analyses de décisions techniques. |

---

## 🚀 Démarrage Rapide

### 1. Démarrage du Dashboard de suivi
```bash
python dashboard/app.py
```
Le tableau de bord de suivi interactif sera accessible sur [http://localhost:5000](http://localhost:5000).
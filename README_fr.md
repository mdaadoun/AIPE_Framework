# 🚀 Standard d'Ingénierie Produit IA (AIPE_Framework) — Framework Industriel & Productivité

[![Python 3.11](https://img.shields.io/badge/python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16.2+-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Poetry](https://img.shields.io/badge/poetry-1.7+-60A5FA?style=flat-square&logo=poetry&logoColor=white)](https://python-poetry.org/)
[![FastAPI 0.110+](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker Multi-Stage](https://img.shields.io/badge/docker-Multi--Stage-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Ruff](https://img.shields.io/badge/linter-Ruff-009688?style=flat-square)](https://github.com/astral-sh/ruff)
[![Mypy strict](https://img.shields.io/badge/typing-Mypy%20strict-blue?style=flat-square)](https://mypy-lang.org/)

[🇬🇧 English version available here](README.md)

**AIPE_Framework** est un socle d'ingénierie logicielle industrielle conçu pour accélérer et sécuriser le développement de projets d'IA appliquée (LLMs, RAG, agents autonomes). Il élimine la dette technique initiale en imposant les meilleures pratiques dès le premier jour (qualité pre-commit, typage strict 100%, conteneurisation sécurisée non-root).

---

## 🎯 Objectifs Métiers & KPIs

* **Onboarding Ultra-Rapide (< 5 min) :** Prise en main zéro-friction (`git clone` $\to$ `make install` $\to$ opérationnel).
* **Isolation du Code :** Séparation stricte entre les expérimentations (`notebooks/`) et le code de production (`src/`).
* **Qualité de Code Systématique :** 100% de couverture de types Mypy dans `src/` couplée à un linting ultra-rapide (< 2s) avec Ruff.
* **Protection des Clés API :** Interception automatique des secrets en clair via des hooks `detect-secrets`.
* **Conteneurisation Optimisée :** Image Docker multi-stage légère (< 250 Mo) sous utilisateur non-root (`appuser` UID 1000).

---

## 📂 Structure du Répertoire

```text
AIPE_Framework/
│
├── README.md                   # Présentation principale en Anglais
├── README_fr.md                # Présentation du framework en Français
│
├── dashboard-next/             # Dashboard interactif Next.js TypeScript & simulateur QA
│   ├── src/app/                # Routes App Router (Présentation, Roadmap, Glossaire, FAQ, Code)
│   └── src/lib/                # Analyseur AST de tests & parser Markdown
│
├── docs/                       # Spécifications et documentation technique
    ├── specifications_fr.md   # Cahier des charges fonctionnel et technique
    ├── roadmap_fr.md          # Feuille de route chronologique en 6 phases
    ├── glossary_fr.md         # Glossaire technique des concepts du framework
    ├── questions_fr.md        # FAQ interactive d'entretien (34 Q&R)
    ├── code_fr.md             # Guide d'architecture du code source
    └── journal_fr.md          # Journal de bord et décisions d'architecture (ADR)
```

---

## 🚀 Démarrage Rapide

### 1. Initialiser le projet
```bash
make install
```

### 2. Lancer le Dashboard Interactif Next.js
```bash
make dashboard
```
Accédez au dashboard sur [http://localhost:3000](http://localhost:3000).

### 3. Exécuter la suite de tests
```bash
make test
```

### 4. Valider le style et les types (Ruff + Mypy)
```bash
make lint
```

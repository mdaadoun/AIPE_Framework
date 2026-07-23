# 📌 Séance 1 : Initialisation de Poetry et du fichier pyproject.toml
**Date :** 23 Juillet 2026

Cette première séance pose les bases du blueprint industriel d'AIPE_Framework. L'objectif est d'implémenter un système déterministe de gestion de dépendances et d'isoler proprement l'environnement virtuel local pour éliminer l'effet "marche sur ma machine".

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **Gestion Déterministe (Poetry) :** Contrairement à un simple `requirements.txt` où les sous-dépendances peuvent changer silencieusement lors de nouvelles installations, Poetry génère un fichier de verrouillage (`poetry.lock`) figeant les versions exactes de tout l'arbre de dépendance.
*   **Séparation des Groupes de Dépendances :** Structuration propre séparant les librairies nécessaires à la production (FastAPI, Pydantic) de celles dédiées uniquement à la qualité et la validation en développement (pytest, ruff, mypy, pre-commit), ce qui allège l'image Docker finale.
*   **Typage Statique Strict (Mypy Strict) :** Règle de développement interdisant l'absence de typage ou le type générique `Any` non explicite dans les signatures de code Python, transformant les avertissements en erreurs bloquantes lors des phases de qualité (Linter).

---

### 2. 🧠 Prises de Décisions & Choix Techniques

#### Dilemme A : Choix du gestionnaire de dépendances
*   **Option A.1 : requirements.txt / pip**  
    *   *Inconvénient :* Manque de locking rigide des dépendances transitives. Pas de séparation native des paquets de dev/prod sans multiplier les fichiers.
*   **Option A.2 : Poetry (Retenue)**  
    *   *Pourquoi ce choix ?* Offre un verrouillage de versioning rigide, isole automatiquement le projet dans un sous-dossier virtuel `.venv` local et permet de configurer tous les outils annexes (Ruff, Mypy) dans un unique fichier `pyproject.toml`.

#### Dilemme B : Choix de la version de Python cible
*   **Option B.1 : Python 3.11**  
    *   *Inconvénient :* Python 3.11 n'est pas disponible par défaut sur la machine physique de l'hôte (qui tourne sous Python 3.10), ce qui empêcherait le bon déroulement de l'onboarding local en moins de 5 minutes.
*   **Option B.2 : Python 3.10 (Retenue)**  
    *   *Pourquoi ce choix ?* Alignement de la cible minimale sur Python 3.10 pour s'adapter à la réalité de l'environnement hôte de développement, tout en conservant une compatibilité ascendante avec Python 3.11+.

---

### 3. 🛠️ Implémentation & Auto-Documentation

Un fichier `pyproject.toml` complet a été créé à la racine de `projets/AIPE_Framework/`. Pour permettre le bon fonctionnement de la commande d'installation éditable de Poetry (`packages = [{include = "src"}]`), un répertoire `src/` et un fichier initial `src/__init__.py` ont été créés.

#### Extrait de configuration `pyproject.toml` :
```toml
[tool.poetry]
name = "aipe-framework"
version = "0.1.0"
description = "Blueprint industriel d'ingénierie logicielle appliquée aux produits IA (AIPE)."
authors = ["Michael <michael@example.com>"]
readme = "README.md"
packages = [{include = "src"}]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.110.0"
uvicorn = {extras = ["standard"], version = "^0.28.0"}
pydantic = "^2.6.4"
```

#### Commandes de validation exécutées :
```bash
# Activation de l'isolation locale
poetry config virtualenvs.in-project true

# Résolution des dépendances et écriture du lockfile
poetry lock

# Installation des dépendances et du code source local dans le .venv
poetry install
```
*Critère de succès :* Les commandes s'exécutent avec succès, créent un dossier `.venv/` à la racine contenant toutes les dépendances compilées, et génèrent un fichier `poetry.lock` cohérent.

---

### 4. 📌 Bilan du Jour

1.  **Création du pyproject.toml** déclarant la configuration de production (FastAPI) et de développement (Ruff, Mypy, Pytest).
2.  **Génération du poetry.lock** figeant de façon immuable l'arbre des versions.
3.  **Initialisation du dossier source `src/`** avec son point d'entrée package `__init__.py`.
4.  **Création du dossier virtuel local `.venv/`** contenant toutes les librairies installées.

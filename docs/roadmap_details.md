# 🗺️ Feuille de Route Détaillée (Roadmap) : AIPE_Framework

Cette feuille de route détaille l'ordre chronologique des étapes pour réaliser le socle technique d'**AIPE_Framework** (Blueprint AI Product Engineering), avec pour chaque étape les concepts théoriques abordés, la progression et les critères de validation.

---

## 📊 Tableau de Bord Synthétique des Phases

```text
Phase 1 : Poetry & Setup ──> Phase 2 : Qualité & Hooks ──> Phase 3 : Interface CLI ──> Phase 4 : API FastAPI ──> Phase 5 : Docker & Sécurité ──> Phase 6 : IDE & Onboarding
     (✅ Validé)                 (🔲 À venir)                (🔲 À venir)             (🔲 À venir)               (🔲 À venir)               (🔲 À venir)
```

---

## Phase 1 : Isolation & Dépendances (Poetry & Setup) — ✅ Validé
*Objectif : Mettre en place un environnement virtuel Python étanche et déterministe.*

### Étape 1.1 : Initialisation Poetry & pyproject.toml — ✅ Validé
*   **Description :** Création du fichier de configuration centralisé [`pyproject.toml`](file:///home/michael/Code/job/projets/AIPE_Framework/pyproject.toml) déclarant les dépendances de production (FastAPI, Uvicorn, Pydantic) et séparant les dépendances de développement (pytest, ruff, mypy, pre-commit).
*   **Concept clé :** Gestion déterministe des dépendances et déclaration sémantique des versions.
*   **Critère de validation :** Le fichier `pyproject.toml` est valide et la commande `poetry install` génère le fichier `poetry.lock`.

### Étape 1.2 : Configuration locale de l'environnement virtuel — ✅ Validé
*   **Description :** Configurer Poetry pour forcer la création de l'environnement virtuel directement à la racine du projet dans un dossier `.venv`. Exclure ce dossier du suivi de version via `.gitignore`.
*   **Concept clé :** Isolation hermétique locale et intégration IDE simplifiée.
*   **Critère de validation :** Un dossier `.venv` local est physiquement créé à la racine du projet et le fichier `.gitignore` l'ignore.

---

## Phase 2 : Gatekeeping & Contrôle Qualité (Pre-commit & Linter) — 🔲 À venir
*Objectif : Mettre en place des barrières de sécurité et d'analyse statique au plus près du commit Git.*

### Étape 2.1 : Configuration Pre-commit & Sécurité — 🔲 À venir
*   **Description :** Initialisation du fichier [`.pre-commit-config.yaml`](file:///home/michael/Code/job/projets/AIPE_Framework/.pre-commit-config.yaml) intégrant des hooks de nettoyage de base et le hook de sécurité passive `detect-secrets`.
*   **Concept clé :** Prévention active des fuites de secrets (API keys OpenAI, Gemini, etc.) dans les dépôts de code.
*   **Critère de validation :** Tenter de commiter un fichier contenant `API_KEY = "sk-proj-12345"` est automatiquement bloqué localement par Git.

### Étape 2.2 : Intégration de Ruff — 🔲 À venir
*   **Description :** Configurer Ruff dans [`pyproject.toml`](file:///home/michael/Code/job/projets/AIPE_Framework/pyproject.toml) avec les jeux de règles standards (E, F, I, B) et l'intégrer au pre-commit.
*   **Concept clé :** Linting et formatage unifiés à haute vitesse.
*   **Critère de validation :** L'analyse statique et le formatage s'exécutent sur l'ensemble des fichiers en moins de 2 secondes.

### Étape 2.3 : Analyse statique avec Mypy (strict) — 🔲 À venir
*   **Description :** Configuration stricte de Mypy dans [`pyproject.toml`](file:///home/michael/Code/job/projets/AIPE_Framework/pyproject.toml) et raccordement au hook pre-commit pour valider le typage statique de l'application.
*   **Concept clé :** Robustesse et vérification formelle des types de données.
*   **Critère de validation :** Tout commit contenant du code Python non-typé ou comportant des incohérences de types dans `src/` échoue.

---

## Phase 3 : Interface de Commande Unifiée (Makefile) — 🔲 À venir
*Objectif : Fournir une interface de commande standardisée éliminant le besoin de retenir des scripts complexes.*

### Étape 3.1 : Automatisation de l'onboarding et du nettoyage — 🔲 À venir
*   **Description :** Rédaction des commandes cibles `make install` (pour initialiser Poetry et installer pre-commit) et `make clean` (pour purger tous les fichiers de cache Python, pytest et mypy) dans le [Makefile](file:///home/michael/Code/job/projets/AIPE_Framework/Makefile).
*   **Concept clé :** standardisation de l'onboarding développeur.
*   **Critère de validation :** La commande `make clean` supprime intégralement les caches sans erreur et `make install` configure tout l'environnement de zéro.

### Étape 3.2 : Intégration des validateurs de test et d'exécution — 🔲 À venir
*   **Description :** Ajout des raccourcis de commande `make lint` (ruff + mypy), `make test` (pytest) et `make dev` (démarrage du serveur web local).
*   **Concept clé :** Abstraction des outils sous-jacents derrière des interfaces stables.
*   **Critère de validation :** Saisir `make lint` ou `make test` exécute les outils internes sans nécessiter d'activer manuellement l'environnement virtuel.

---

## Phase 4 : API FastAPI Base & Healthcheck — 🔲 À venir
*Objectif : Mettre en place le microservice web minimaliste de production.*

### Étape 4.1 : Initialisation de l'API et structure de paquets — 🔲 À venir
*   **Description :** Création du dossier [`src/`](file:///home/michael/Code/job/projets/AIPE_Framework/src/) avec un fichier [`__init__.py`](file:///home/michael/Code/job/projets/AIPE_Framework/src/__init__.py) propre et le point d'entrée [`main.py`](file:///home/michael/Code/job/projets/AIPE_Framework/src/main.py) initialisant FastAPI.
*   **Concept clé :** Serveur d'API asynchrone ASGI.
*   **Critère de validation :** Le serveur se lance localement via la commande `make dev` sur le port 8000.

### Étape 4.2 : Implémentation du Healthcheck conforme — 🔲 À venir
*   **Description :** Ajout de la route de santé `/health` renvoyant le schéma JSON requis contenant `status`, `environment`, et `version` (0.1.0).
*   **Concept clé :** Contrat d'interface et observabilité minimale.
*   **Critère de validation :** Un appel GET sur `http://localhost:8000/health` renvoie exactement le payload JSON ciblé.

### Étape 4.3 : Suite de tests unitaires d'API — 🔲 À venir
*   **Description :** Création de [`tests/test_main.py`](file:///home/michael/Code/job/projets/AIPE_Framework/tests/test_main.py) utilisant `fastapi.testclient` et validation de la route de santé.
*   **Concept clé :** Test d'intégration automatisé.
*   **Critère de validation :** L'exécution de `make test` renvoie 100% de réussite avec couverture complète.

---

## Phase 5 : Conteneurisation de Production & Hardening (Docker) — 🔲 À venir
*Objectif : Créer une image de conteneur ultra-légère et hautement sécurisée.*

### Étape 5.1 : Dockerfile Multi-stage avec Poetry — 🔲 À venir
*   **Description :** Écriture du [`Dockerfile`](file:///home/michael/Code/job/projets/AIPE_Framework/Dockerfile) composé d'un stage `builder` (installation de Poetry et compilation des dépendances dans un `.venv` interne) et d'un stage `runtime` (copie du `.venv` et du code source uniquement).
*   **Concept clé :** Séparation des outils de compilation du runtime final (réduction de surface d'attaque).
*   **Critère de validation :** Le build de l'image se termine avec succès et produit une image d'un poids inférieur à 250 Mo.

### Étape 5.2 : Sécurisation Non-root (Hardening) — 🔲 À venir
*   **Description :** Créer un utilisateur non-privilégié `appuser` dans le conteneur final et lui transférer les droits de possession sur les fichiers exécutables de l'application.
*   **Concept clé :** Principe de moindre privilège appliqué à l'exécution de conteneurs.
*   **Critère de validation :** Lancer le conteneur et inspecter le processus en cours d'exécution confirme que le serveur tourne sous l'identité de `appuser` (UID 1000) et non `root`.

### Étape 5.3 : Sonde de surveillance système (Healthcheck) — 🔲 À venir
*   **Description :** Ajouter la clause `HEALTHCHECK` dans le Dockerfile interrogeant l'API locale `/health` toutes les 15 secondes à l'aide de `curl`.
*   **Concept clé :** Healthchecking conteneur natif pour l'orchestration (K8s, ECS, Cloud Run).
*   **Critère de validation :** La commande `docker ps` affiche le statut `(healthy)` après le démarrage du conteneur.

---

## Phase 6 : Intégration IDE & Validation Finale — 🔲 À venir
*Objectif : Valider l'expérience globale du développeur et de la chaîne d'outils.*

### Étape 6.1 : Configuration de l'environnement IDE — 🔲 À venir
*   **Description :** Création du fichier de paramètres VSCode `.vscode/settings.json` pour configurer le formatage automatique à la sauvegarde via le formateur officiel de Ruff.
*   **Concept clé :** Alignement de l'environnement de développement et de la CI locale.
*   **Critère de validation :** Sauvegarder un fichier Python mal formaté dans VSCode applique instantanément la correction.

### Étape 6.2 : Simulation d'onboarding ("Zero-Setup Friction") — 🔲 À venir
*   **Description :** Valider la procédure complète de déploiement à partir d'un clonage propre dans un dossier temporaire.
*   **Concept clé :** Métrique KPI d'onboarding.
*   **Critère de validation :** Un développeur externe clone le projet, exécute `make install` et démarre le serveur avec `make dev` en moins de 5 minutes chrono.

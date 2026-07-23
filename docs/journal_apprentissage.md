# 📓 Journal d'Apprentissage : Blueprint AI Product Engineering

Ce journal documente les séances de cadrage, de conception et les décisions d'architecture prises lors de la spécification de ce framework.

---

## 📅 Séance 1 : Cadrage Stratégique & Choix d'Architecture (23 Juillet 2026)

### Objectif de la séance
Définir le socle technique standardisé pour éliminer la dette technique sur les projets IA.

### Sujets abordés & Dilemmes techniques
1.  **Gestionnaire de dépendances : requirements.txt vs Poetry**
    *   * requirements.txt :* Simple, mais instable en cas de dépendances transitives non verrouillées.
    *   * Poetry :* Plus complexe au début, mais assure le déterminisme (`poetry.lock`) et gère nativement le packaging et les groupes de dépendances (dev vs main).
    *   * Décision :* Choix unanime de **Poetry** pour sa robustesse et sa reproductibilité en production.
2.  **Linter & Formateur : Ruff vs Outils Historiques (Black + Flake8)**
    *   * Constat :* Avoir 4 outils séparés ralentit le pipeline pre-commit locale et multiplie les fichiers de config.
    *   * Décision :* Intégration de **Ruff** uniquement. Ses performances écrites en Rust et son formateur intégré simplifient la stack logicielle.

### Décisions Clés (ADRs)
*   Imposer le typage statique strict avec **Mypy** dans `src/` pour sécuriser les interfaces d'API.
*   Centraliser l'intégralité de la configuration des outils de build dans le fichier unique `pyproject.toml`.

---

## 📅 Séance 2 : Sécurisation & Contrôle Qualité local (23 Juillet 2026)

### Objectif de la séance
Mettre en place des mécanismes pour empêcher l'envoi de secrets (API Keys) et de code mal formaté sur le dépôt partagé.

### Sujets abordés & Dilemmes techniques
1.  **Interception des secrets : detect-secrets en CI vs local pre-commit**
    *   * Constat :* Si le secret est poussé sur le serveur, il est déjà compromis dans l'historique Git.
    *   * Décision :* Installer `detect-secrets` en local via **pre-commit**. Le blocage se fait directement sur le poste du développeur avant la création physique du commit Git.
2.  **Interface de Commande Unifiée (Makefile)**
    *   * Constat :* Les commandes Poetry et Git-hooks peuvent être difficiles à retenir pour un nouveau développeur.
    *   * Décision :* Définir un **Makefile** avec 5 cibles standardisées (`install`, `lint`, `test`, `dev`, `clean`) pour réduire le temps de mise en route de 30 minutes à moins de 5 minutes.

---

## 📅 Séance 3 : Conteneurisation de Production Hardened (23 Juillet 2026)

### Objectif de la séance
Concevoir l'image Docker de production pour qu'elle soit la plus légère et sécurisée possible.

### Sujets abordés & Dilemmes techniques
1.  **Optimisation de la taille : Image python-slim classique vs Multi-Stage Build**
    *   * Constat :* Installer Poetry et les compilateurs système dans le conteneur final double la taille de l'image.
    *   * Décision :* Utilisation d'un **build multi-stage**. Le stage `builder` compile et prépare l'environnement virtuel `.venv`, tandis que le stage `runtime` se contente de copier ce dossier virtuel, gardant l'image finale sous la barre des 250 Mo.
2.  **Hardening de Sécurité**
    *   * Constat :* Par défaut, les conteneurs Docker s'exécutent sous l'utilisateur root, ce qui représente un risque majeur d'élévation de privilèges en cas d'intrusion.
    *   * Décision :* Création d'un utilisateur non-privilégié `appuser` (UID 1000) et transfert des droits sur les répertoires applicatifs. L'application s'exécute ainsi avec le niveau de privilèges minimal.

---

## 📅 Séance 4 : Validation du Gatekeeping & Intégration Dashboard (23 Juillet 2026)

### Objectif de la séance
Automatiser la validation du fonctionnement des outils de gatekeeping (detect-secrets, Ruff, Mypy) et les intégrer de façon transparente dans l'interface de test du dashboard.

### Sujets abordés & Dilemmes techniques
1.  **Tests unitaires de l'outillage de qualité (Tooling Testing)**
    *   * Constat :* Les modifications manuelles de configuration peuvent dégrader silencieusement les barrières de qualité.
    *   * Décision :* Écriture d'une suite de tests pytest (`tests/test_gatekeeping.py`) qui injecte volontairement des erreurs (secrets exposés, mauvais formatage, absence de types) pour s'assurer que les validateurs réagissent et échouent comme prévu.
2.  **Gestion des environnements de test de detect-secrets**
    *   * Constat :* L'utilisation du dossier `/tmp` système provoquait des faux négatifs (non-détection du secret) car `detect-secrets` filtre les répertoires en dehors du dépôt Git.
    *   * Décision :* Écriture temporaire du fichier secret directement dans le sous-dossier `tests/` et nettoyage automatique par une clause `finally` pour garantir la détection par rapport au dépôt actif.

### Décisions Clés (ADRs)
*   Ajout automatique de `tests/test_gatekeeping.py` à la liste des tests du dashboard pour permettre son lancement à la demande par les développeurs.

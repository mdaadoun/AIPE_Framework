# 📖 Glossaire Technique : Blueprint AI Product Engineering

Ce glossaire définit les concepts clés de l'ingénierie logicielle et du DevOps appliqués à l'industrialisation des projets d'intelligence artificielle dans ce framework.

---

## 🛠️ Outillage & Environnements

### Poetry
Outil moderne de gestion des dépendances et d'empaquetage en Python. Contrairement à `pip` et `requirements.txt`, **Poetry** résout de manière déterministe les arbres de dépendances complexes et verrouille les versions exactes dans un fichier `poetry.lock`. Cela garantit que tous les développeurs et serveurs de CI exécutent exactement le même code.

### Environnement Virtuel (`.venv`)
Dossier isolé contenant l'exécutable Python et les bibliothèques installées spécifiquement pour le projet. Dans ce framework, l'environnement virtuel est configuré localement à la racine (`.venv/`) pour simplifier la détection et l'intégration par l'IDE (comme VSCode ou PyCharm).

### Makefile
Fichier de configuration de l'utilitaire système `make` (standard POSIX). Il permet de définir des alias de commandes standardisées (`make install`, `make test`, `make lint`) afin d'offrir une interface unifiée aux développeurs, facilitant l'onboarding et l'intégration continue.

---

## 🔍 Qualité & Analyse Statique

### Ruff
Linter et formateur de code Python ultra-rapide écrit en Rust. Il remplace avantageusement des outils plus anciens comme Flake8, Black, isort et autoflake. Ruff permet d'analyser le code et d'appliquer le formatage en moins d'une seconde, accélérant la boucle de feedback locale.

### Mypy
Vérificateur de typage statique pour Python. Bien que Python soit un langage à typage dynamique, l'utilisation d'annotations de type validées par Mypy (en mode strict) élimine toute une classe d'erreurs en production avant même que le code ne soit exécuté (ex. passage de types invalides, manipulation d'éléments `None`).

### Pre-commit Hooks
Mécanisme Git permettant d'exécuter des scripts automatiquement au moment de la commande `git commit`. Si l'un des scripts échoue (code mal formaté, erreurs de typage ou faille de sécurité), le commit est bloqué localement, protégeant ainsi l'intégrité du dépôt partagé.

---

## 🔒 Sécurité & DevOps

### detect-secrets
Outil d'analyse statique conçu pour détecter les clés d'API (OpenAI, Gemini), les mots de passe et les jetons d'accès codés en dur dans le code source. Configuré en hook pre-commit, il intercepte instantanément les tentatives de commit de clés privées.

### Docker Multi-Stage Build
Technique de build Docker permettant d'utiliser plusieurs instructions `FROM` temporaires dans un même `Dockerfile`. Elle permet d'installer les compilateurs et les dépendances lourdes dans un premier conteneur (stage `builder`), puis de copier uniquement le résultat compilé dans le conteneur final (stage `runtime`), réduisant ainsi le poids de l'image de 80% et limitant la surface d'attaque.

### Hardening Non-Root
Pratique de sécurité consistant à forcer l'exécution de l'application dans le conteneur Docker sous un utilisateur système non-privilégié (`appuser`) plutôt que sous l'utilisateur `root`. En cas de compromission de l'application, l'attaquant n'obtient pas les droits super-utilisateur sur la machine hôte.

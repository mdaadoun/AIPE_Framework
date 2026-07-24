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

### Cibles Phony (`.PHONY`)
Directive dans un Makefile spécifiant que les cibles listées ne correspondent pas à des fichiers physiques sur le disque. Cela évite les conflits de noms si un dossier ou un fichier portant le même nom venait à être créé (par exemple, un dossier `test/`).

### Zero-Setup Friction
Indicateur de performance (KPI) mesurant l'effort nécessaire à l'installation d'un environnement de développement complet. L'objectif est de permettre à un nouveau venu d'être pleinement opérationnel en une seule commande standard (`make install`) en moins de 5 minutes.

---

## 🔍 Qualité & Analyse Statique

### Ruff
Linter et formateur de code Python ultra-rapide écrit en Rust. Il remplace avantageusement des outils plus anciens comme Flake8, Black, isort et autoflake. Ruff permet d'analyser le code et d'appliquer le formatage en moins d'une seconde, accélérant la boucle de feedback locale.

### Mypy
Vérificateur de typage statique pour Python. Bien que Python soit un langage à typage dynamique, l'utilisation d'annotations de type validées par Mypy (en mode strict) élimine toute une classe d'erreurs en production avant même que le code ne soit exécuté (ex. passage de types invalides, manipulation d'éléments `None`).

### Analyse Statique de Type (Type Hinting - PEP 484)
Annotation explicite des types de données pour les arguments de fonctions, variables et valeurs de retour. Validée en phase de build (par Mypy), elle sert de documentation vivante et prévient les bugs d'exécution sans imposer de surcharge de performances à l'exécution.

### Pre-commit Hooks
Mécanisme Git permettant d'exécuter des scripts automatiquement au moment de la commande `git commit`. Si l'un des scripts échoue (code mal formaté, erreurs de typage ou faille de sécurité), le commit est bloqué localement, protégeant ainsi l'intégrité du dépôt partagé.

---

## 🔒 Sécurité & DevOps

### detect-secrets
Outil d'analyse statique conçu pour détecter les clés d'API (OpenAI, Gemini), les mots de passe et les jetons d'accès codés en dur dans le code source. Configuré en hook pre-commit, il intercepte instantanément les tentatives de commit de clés privées.

### Baseline de secrets (`.secrets.baseline`)
Fichier JSON généré à la racine du dépôt contenant les empreintes (hashes) des secrets ou des faux secrets de test identifiés et approuvés. Ce fichier sert de référence à `detect-secrets` pour ne signaler que les *nouveaux* secrets accidentellement ajoutés, évitant de bloquer le pipeline à cause de mocks existants.

### Docker Multi-Stage Build
Technique de build Docker permettant d'utiliser plusieurs instructions `FROM` temporaires dans un même `Dockerfile`. Elle permet d'installer les compilateurs et les dépendances lourdes dans un premier conteneur (stage `builder`), puis de copier uniquement le résultat compilé dans le conteneur final (stage `runtime`), réduisant ainsi le poids de l'image de 80% et limitant la surface d'attaque.

### Hardening Non-Root
Pratique de sécurité consistant à forcer l'exécution de l'application dans le conteneur Docker sous un utilisateur système non-privilégié (`appuser`) plutôt que sous l'utilisateur `root`. En cas de compromission de l'application, l'attaquant n'obtient pas les droits super-utilisateur sur la machine hôte.

### Dockerfile
Fichier texte contenant une série d'instructions ordonnées (`FROM`, `COPY`, `RUN`, `CMD`) décrivant comment assembler une image Docker couche par couche. Chaque instruction crée une nouvelle couche immuable dans l'image, empilée sur la précédente. Le Dockerfile est le « plan de construction » de l'environnement d'exécution de l'application.

### Couche Docker (Layer) et cache de build
Chaque instruction d'un Dockerfile (`RUN`, `COPY`, etc.) produit une couche (layer) immuable. Docker met en cache ces couches et les réutilise si les fichiers d'entrée n'ont pas changé. C'est pourquoi l'ordre des instructions est stratégique : copier les fichiers de dépendances (`pyproject.toml`, `poetry.lock`) *avant* le code source permet de réutiliser la couche d'installation des paquets lors des modifications de code, accélérant les rebuilds de plusieurs minutes à quelques secondes.

### Contexte de build Docker (Build Context)
Ensemble de tous les fichiers et dossiers envoyés au démon Docker au moment du `docker build`. Par défaut, c'est l'intégralité du répertoire courant. Un contexte trop volumineux (contenant `.venv`, `.git`, `node_modules`) ralentit le transfert et risque d'inclure des fichiers sensibles dans l'image. Le fichier `.dockerignore` sert à filtrer ce contexte.

### .dockerignore
Fichier de configuration fonctionnant comme `.gitignore`, mais pour Docker. Il spécifie les fichiers et dossiers à exclure du contexte de build. Les exclusions typiques incluent l'environnement virtuel local (`.venv`), l'historique Git (`.git`), les tests, la documentation et les caches de développement. Un `.dockerignore` bien configuré peut réduire le contexte de build de plusieurs centaines de Mo à quelques Ko.

### COPY --from (Copie inter-stages)
Instruction Docker spécifique au pattern multi-stage build permettant de copier sélectivement des fichiers depuis un stage précédent vers le stage courant. La syntaxe `COPY --from=builder /app/.venv /app/.venv` copie uniquement l'environnement virtuel compilé depuis le stage `builder` vers l'image finale, sans embarquer les outils de compilation qui ont servi à le créer.

---

## 🌐 Architecture Web & Microservices

### FastAPI
Framework web moderne, rapide et performant pour concevoir des API en Python. Il s'appuie sur le typage statique standard et Pydantic pour automatiser la validation à l'exécution et générer de manière interactive la documentation OpenAPI (/docs).

### ASGI (Asynchronous Server Gateway Interface)
Standard moderne de serveurs web Python succédant à WSGI. Il gère l'asynchronisme de manière native (async/await), ce qui est indispensable pour des cas d'usage à forte concurrence (comme les connexions WebSocket ou le streaming de réponses d'agents d'IA).

### Pydantic
Bibliothèque de validation de données s'appuyant sur les indices de types de Python. Utilisée par FastAPI, elle parse, valide et convertit les types à l'entrée et à la sortie des routes d'API, garantissant un typage strict et une détection précoce des données mal formées.

### APIRouter
Composant de FastAPI servant à modulariser les points d'accès (endpoints) de l'API. Il permet de regrouper et d'isoler des ensembles cohérents de routes (ex: toutes les routes liées à la santé `/health`, au RAG, ou aux agents d'IA) dans des fichiers dédiés pour éviter d'encombrer le point d'entrée central `main.py`.

### Séparation des préoccupations (Separation of Concerns - SoC)
Principe d'architecture logicielle stipulant que le code doit être scindé en sections distinctes, chacune gérant une responsabilité unique. Dans ce framework, cela se traduit par le découpage en configurations (`core`), modèles de données (`schemas`), routes (`api/routes`), et logique d'initialisation (`main.py`).

### Pattern Settings
Pratique d'ingénierie consistant à centraliser toutes les variables de configuration et métadonnées d'une application dans un objet ou une classe unique (souvent couplée à des variables d'environnement). Cela facilite la portabilité et le déploiement du code sur différents environnements (développement, staging, production) sans modifier le code métier.

### Contrat d'interface
Spécification technique rigoureuse qui décrit la structure, les types de données, les codes de statut HTTP et le comportement d'un point d'accès d'une API. Le respect strict de ce contrat garantit la compatibilité et la communication entre les différents services d'un système distribué (ex: microservices, applications frontales).

### Observabilité
Capacité à mesurer et à déduire l'état interne d'un système à partir de ses sorties externes (journaux, métriques, traces et endpoints de santé). Une observabilité minimale permet aux systèmes d'orchestration ou de surveillance de s'assurer du fonctionnement correct et continu de l'application.

### Sonde de santé (Healthcheck Probe)
Mécanisme automatique de test périodique effectuant des requêtes sur un conteneur ou un service (souvent sur la route `/health`) pour surveiller son état de disponibilité et de fonctionnement. Ces sondes sont utilisées par les orchestrateurs (Docker, Kubernetes) pour piloter le routage du trafic et gérer le cycle de vie des conteneurs.

### Test d'intégration
Technique de test consistant à valider le fonctionnement conjoint de plusieurs composants ou modules d'une application (ex: le serveur d'API, le middleware, les configurations et la sérialisation des schémas), par opposition aux tests unitaires qui vérifient des isolats de fonctions logiques.

### Couverture de code (Code Coverage)
Mesure statistique (exprimée en pourcentage) qui comptabilise le taux de lignes de code exécutées lors du lancement de la suite de tests. Imposer un taux minimal strict (ex: 100% via fail-under) garantit qu'aucune modification de code n'est poussée en production sans validation automatique associée.

### TestClient
Utilitaire fourni par la bibliothèque Starlette qui permet d'exécuter des tests d'intégration HTTP rapides sur une application FastAPI en simulant des requêtes (GET, POST, etc.) en boucle locale fermée, éliminant ainsi le besoin de démarrer un serveur réseau réel.

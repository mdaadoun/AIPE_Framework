# ==============================================================================
# Dockerfile - Image de Production Multi-Stage pour AIPE_Framework
# ==============================================================================
# Ce fichier utilise le pattern Docker "Multi-Stage Build" pour produire une
# image finale ultra-légère et sécurisée. L'idée est simple :
#
#   Stage 1 (builder) : On installe tous les outils lourds (Poetry, compilateurs)
#                        nécessaires pour assembler les dépendances Python.
#   Stage 2 (runtime) : On copie UNIQUEMENT le résultat compilé (le dossier .venv)
#                        et le code source dans une image Python nue et minimale.
#                        On y ajoute le hardening non-root (appuser, UID 1000)
#                        et une sonde de surveillance native (HEALTHCHECK).
#
# Résultat : l'image finale ne contient ni Poetry, ni pip, ni gcc, ni aucun outil
# de compilation. Elle est donc plus légère (~150 Mo vs ~1 Go) et présente une
# surface d'attaque réduite (moins de binaires exploitables par un attaquant).
# ==============================================================================


# ==============================================================================
# STAGE 1 : BUILDER — Installation de Poetry et compilation des dépendances
# ==============================================================================
# On utilise l'image officielle Python 3.10 en version "slim" (basée sur Debian
# allégé) car elle contient les en-têtes C nécessaires à la compilation de
# certaines bibliothèques Python natives (comme uvloop utilisé par Uvicorn).
# Le suffixe "slim" signifie que les paquets non-essentiels (man pages, docs,
# éditeurs de texte) ont été retirés pour réduire le poids de base.
FROM python:3.10-slim AS builder

# --- Variable d'environnement de contrôle de Poetry ---
# POETRY_VERSION : Fige la version exacte de Poetry installée pour garantir
#                  la reproductibilité du build (évite les surprises si une
#                  nouvelle version de Poetry change un comportement).
ENV POETRY_VERSION=1.8.2

# POETRY_HOME : Spécifie le répertoire d'installation de Poetry lui-même.
#               En l'isolant dans /opt/poetry, on évite tout conflit avec
#               les paquets Python du système ou du projet.
ENV POETRY_HOME=/opt/poetry

# POETRY_VIRTUALENVS_IN_PROJECT : Force Poetry à créer l'environnement virtuel
#                                 directement dans le dossier du projet sous
#                                 /app/.venv au lieu du cache utilisateur.
#                                 C'est crucial pour pouvoir copier proprement
#                                 ce dossier .venv vers le stage runtime.
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# POETRY_NO_INTERACTION : Désactive les invites interactives de Poetry (choix
#                          de version, confirmations). Indispensable en mode
#                          automatisé (Docker build, CI/CD) où personne ne peut
#                          taper de réponse dans un terminal.
ENV POETRY_NO_INTERACTION=1

# Ajoute le binaire 'poetry' au PATH système pour pouvoir l'appeler directement
# sans préfixer le chemin complet /opt/poetry/bin/poetry.
ENV PATH="${POETRY_HOME}/bin:${PATH}"

# --- Installation de Poetry via le script officiel ---
# On utilise le script d'installation officiel (install.python-poetry.org) plutôt
# que 'pip install poetry' pour deux raisons :
#   1. Isolation : Poetry s'installe dans son propre répertoire (/opt/poetry),
#      sans polluer l'environnement Python du projet.
#   2. Reproductibilité : Le script gère proprement le pinning de version.
#
# 'curl' est installé temporairement car l'image slim ne l'inclut pas par défaut.
# On nettoie les caches apt après l'installation pour ne pas gonfler la couche
# Docker inutilement.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get purge -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# --- Copie des fichiers de manifeste de dépendances ---
# On copie UNIQUEMENT pyproject.toml et poetry.lock AVANT le code source.
# C'est une optimisation importante du cache Docker :
#   - Si seul le code source change (sans toucher aux dépendances), Docker
#     réutilise la couche mise en cache de 'poetry install' et n'a pas besoin
#     de retélécharger les paquets. Cela accélère drastiquement les rebuilds.
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# --- Installation des dépendances de production uniquement ---
# '--only main' : N'installe que les dépendances déclarées dans la section
#                 [tool.poetry.dependencies] (FastAPI, Uvicorn, Pydantic).
#                 Les dépendances de développement (pytest, ruff, mypy) sont
#                 exclues car elles sont inutiles et même nuisibles en production.
# '--no-root'   : N'installe pas le paquet du projet lui-même (juste ses
#                 dépendances). Notre code source sera copié séparément.
RUN poetry install --only main --no-root

# --- Copie du code source de l'application ---
# On copie le code source après l'installation des dépendances pour bénéficier
# au maximum du cache Docker (voir explication ci-dessus).
COPY src/ ./src/


# ==============================================================================
# STAGE 2 : RUNTIME — Image finale ultra-légère de production
# ==============================================================================
# On repart d'une image Python 3.10-slim VIERGE. Rien du stage builder
# (Poetry, curl, caches pip) n'est présent ici. On ne copie que le strict
# nécessaire : l'environnement virtuel compilé et le code source.
FROM python:3.10-slim AS runtime

# Métadonnées OCI (Open Container Initiative) standardisées.
# Ces labels sont lisibles par les registres de conteneurs (Docker Hub, GCR,
# ECR) et les outils de supervision pour identifier l'image.
LABEL maintainer="Michael <michael@example.com>"
LABEL description="AIPE_Framework — Microservice FastAPI de production (Blueprint AI Product Engineering)"
LABEL version="0.1.0"

# --- Variables d'environnement de l'application ---
# PYTHONDONTWRITEBYTECODE : Empêche Python de générer des fichiers .pyc
#                           (bytecode compilé) dans le conteneur. Ces fichiers
#                           sont inutiles en production containerisée car le
#                           code n'est jamais modifié après le déploiement.
ENV PYTHONDONTWRITEBYTECODE=1

# PYTHONUNBUFFERED : Force Python à écrire les sorties (print, logs) directement
#                    dans stdout/stderr sans les mettre en tampon (buffer).
#                    C'est indispensable pour que les orchestrateurs (Docker,
#                    Kubernetes) puissent lire les logs en temps réel.
ENV PYTHONUNBUFFERED=1

# PATH : Ajoute le dossier bin de l'environnement virtuel copié au PATH.
#         Cela permet d'appeler 'uvicorn' directement sans préfixer le chemin
#         complet /app/.venv/bin/uvicorn.
ENV PATH="/app/.venv/bin:${PATH}"

# Définit le répertoire de travail par défaut dans le conteneur.
WORKDIR /app

# ==============================================================================
# ÉTAPE 5.3 : INSTALLATION DE CURL POUR LA SONDE DE SANTÉ (HEALTHCHECK)
# ==============================================================================
# L'image python:3.10-slim ne contient pas d'outil de transfert HTTP (ni curl,
# ni wget). Or, la sonde de santé Docker HEALTHCHECK a besoin d'un client HTTP
# pour interroger l'endpoint /health de notre API.
#
# On installe curl de façon minimale :
#   '--no-install-recommends' évite les paquets optionnels (gain ~20 Mo).
#   'rm -rf /var/lib/apt/lists/*' nettoie le cache APT pour ne pas gonfler
#   la couche Docker.
#
# Note importante : cette installation doit être faite AVANT la directive
# 'USER appuser', car apt-get nécessite les privilèges root pour fonctionner.
# ==============================================================================
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# ==============================================================================
# ÉTAPE 5.2 : SÉCURISATION NON-ROOT (HARDENING)
# ==============================================================================
# Principe de moindre privilège ("Least Privilege") :
# Par défaut, un conteneur Docker exécute tout en tant que 'root' (UID 0).
# C'est dangereux car si un attaquant exploite une faille dans l'application
# (ex: injection de commande, traversée de répertoire), il obtient les droits
# root à l'intérieur du conteneur. Avec certaines configurations Docker mal
# sécurisées, cela peut même permettre de s'échapper du conteneur et
# compromettre la machine hôte.
#
# La solution : créer un utilisateur système non-privilégié ('appuser') et
# exécuter l'application sous son identité. Ainsi, même en cas de compromission,
# l'attaquant n'a que des droits limités (pas d'installation de paquets,
# pas de modification des fichiers système, pas d'accès aux processus d'autres
# conteneurs).
# ==============================================================================

# --- Création du groupe et de l'utilisateur non-privilégié ---
# 'addgroup --system appgroup' : Crée un groupe système (sans répertoire home,
#   sans shell de connexion). Les groupes système sont réservés aux services
#   et démons, pas aux utilisateurs humains.
# 'adduser --system --uid 1000 --ingroup appgroup --no-create-home appuser' :
#   Crée un utilisateur système avec un UID fixe de 1000 (convention standard
#   pour le premier utilisateur non-root dans les conteneurs). L'option
#   '--no-create-home' évite de créer un répertoire /home/appuser inutile.
#   L'option '--ingroup appgroup' associe cet utilisateur au groupe créé.
#
# Pourquoi un UID fixe à 1000 ?
#   En production, les orchestrateurs (Kubernetes, ECS) peuvent imposer des
#   contraintes de sécurité (PodSecurityPolicy, SecurityContext) interdisant
#   l'exécution avec un UID < 1000. Fixer l'UID garantit la compatibilité
#   avec ces politiques de sécurité d'entreprise.
RUN addgroup --system appgroup \
    && adduser --system --uid 1000 --ingroup appgroup --no-create-home appuser

# --- Copie chirurgicale depuis le stage builder avec transfert de propriété ---
# '--from=builder' : Instruction Docker multi-stage qui copie des fichiers
#                     depuis le stage nommé 'builder' (défini plus haut).
# '--chown=appuser:appgroup' : Transfère directement la propriété des fichiers
#   copiés à l'utilisateur 'appuser' et au groupe 'appgroup'. Sans cette option,
#   les fichiers copiés appartiendraient à root, et appuser ne pourrait pas les
#   lire ou les exécuter correctement.
#
# On ne copie que deux éléments :
#   1. /app/.venv : L'environnement virtuel contenant toutes les dépendances
#                   Python compilées (FastAPI, Uvicorn, Pydantic et leurs
#                   sous-dépendances). C'est le résultat de 'poetry install'.
#   2. /app/src   : Le code source de notre application.
#
# Tout le reste (Poetry, curl, caches pip, fichiers temporaires) est abandonné
# avec le stage builder et n'apparaît jamais dans l'image finale.
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/src /app/src

# --- Basculement vers l'utilisateur non-privilégié ---
# À partir de cette instruction, TOUTES les commandes suivantes (CMD, ENTRYPOINT)
# seront exécutées sous l'identité de 'appuser' (UID 1000) et non plus 'root'.
# C'est le verrou final du hardening : même si un attaquant accède au conteneur,
# il n'a aucun droit administrateur.
USER appuser

# --- Exposition du port réseau ---
# EXPOSE documente le port sur lequel le conteneur écoute. Cette instruction
# est purement informative (elle n'ouvre pas réellement le port). Elle sert
# de documentation pour les développeurs et les outils d'orchestration.
#
# Note de sécurité : Le port 8000 est un port non-privilégié (> 1024).
# C'est important car seul 'root' peut ouvrir des ports < 1024 (ports
# privilégiés comme 80 ou 443). Notre choix du port 8000 est donc compatible
# avec l'exécution en tant que 'appuser'.
EXPOSE 8000

# ==============================================================================
# ÉTAPE 5.3 : SONDE DE SURVEILLANCE SYSTÈME (HEALTHCHECK)
# ==============================================================================
# L'instruction HEALTHCHECK configure Docker pour tester automatiquement si
# l'application à l'intérieur du conteneur fonctionne correctement.
#
# C'est comme un médecin qui prend le pouls d'un patient à intervalles
# réguliers : si le pouls s'arrête (l'API ne répond plus), l'alarme se
# déclenche et les mesures correctives sont prises automatiquement.
#
# Fonctionnement :
#   1. Docker exécute la commande 'curl' toutes les 15 secondes (--interval).
#   2. Si l'API répond avec un code HTTP 2xx, le conteneur est marqué 'healthy'.
#   3. Si curl échoue ou que l'API met plus de 5 secondes à répondre (--timeout),
#      Docker compte un échec.
#   4. Après 3 échecs consécutifs (--retries), le conteneur passe à 'unhealthy'.
#   5. Le premier test est retardé de 10 secondes (--start-period) pour laisser
#      à Uvicorn le temps de démarrer complètement.
#
# Utilité en production :
#   - Docker Swarm redémarre automatiquement les conteneurs 'unhealthy'.
#   - Kubernetes utilise cette information pour ses propres sondes (liveness).
#   - 'docker ps' affiche le statut (healthy) à côté du conteneur.
#   - Les outils de monitoring (Prometheus, Grafana) peuvent exploiter cet état.
#
# Options détaillées :
#   --interval=15s    : Fréquence des vérifications (toutes les 15 secondes).
#   --timeout=5s      : Temps maximum accordé à curl pour obtenir une réponse.
#   --start-period=10s: Délai de grâce après le démarrage du conteneur pendant
#                       lequel les échecs ne comptent pas (le temps qu'Uvicorn
#                       charge les modules Python et commence à servir).
#   --retries=3       : Nombre d'échecs consécutifs avant de déclarer le
#                       conteneur 'unhealthy'.
#
# 'curl -f' : L'option '-f' (fail silently) fait échouer curl avec un code
#             de sortie non-nul si le serveur renvoie un code HTTP d'erreur
#             (4xx ou 5xx). Sans cette option, curl renverrait un succès même
#             si l'API répond 500 Internal Server Error.
# '|| exit 1': Si curl échoue pour une raison quelconque (serveur injoignable,
#              timeout, erreur réseau), on force un code de sortie 1 pour que
#              Docker comptabilise l'échec.
# ==============================================================================
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# --- Commande de démarrage du serveur de production ---
# CMD définit la commande exécutée au lancement du conteneur.
# 'uvicorn' : Serveur ASGI haute performance qui héberge notre application FastAPI.
# 'src.main:app' : Chemin Python vers l'objet FastAPI (module src.main, variable app).
# '--host 0.0.0.0' : Écoute sur toutes les interfaces réseau du conteneur
#                     (nécessaire pour que le trafic externe puisse atteindre
#                     le serveur à l'intérieur du conteneur Docker).
# '--port 8000' : Port d'écoute interne au conteneur.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

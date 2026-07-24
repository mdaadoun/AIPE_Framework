"""Tests de validation du Dockerfile Multi-Stage et de la configuration Docker.

Ce module vérifie la présence, la structure et la conformité du Dockerfile
multi-stage produit aux étapes 5.1 et 5.2 du blueprint AIPE_Framework.

Étape 5.1 : Valide le pattern multi-stage build (deux stages, exclusion des
    outils de développement, fichier .dockerignore).
Étape 5.2 : Valide le hardening non-root (création de l'utilisateur appuser,
    transfert de propriété via --chown, directive USER, ordonnancement correct).
"""

from pathlib import Path

# Chemin absolu vers la racine du projet AIPE_Framework
PROJECT_DIR = Path(__file__).resolve().parent.parent


def test_dockerfile_exists() -> None:
    """Vérifie que le fichier Dockerfile est physiquement présent à la racine du projet."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    assert dockerfile.exists(), (
        "Le fichier 'Dockerfile' est introuvable à la racine du projet. "
        "Il doit être créé pour conteneuriser l'application."
    )
    assert (
        dockerfile.stat().st_size > 0
    ), "Le fichier 'Dockerfile' existe mais est vide."


def test_dockerfile_has_multi_stage_build() -> None:
    """Vérifie que le Dockerfile contient bien deux stages distincts (builder + runtime).

    Le pattern multi-stage nécessite au minimum deux instructions FROM :
    - Un premier FROM ... AS builder pour installer Poetry et compiler les dépendances.
    - Un second FROM ... AS runtime pour produire l'image finale allégée.
    """
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    # Vérification du stage builder
    assert "AS builder" in content, (
        "Le Dockerfile ne contient pas de stage 'builder'. "
        "Un build multi-stage nécessite un premier stage nommé 'AS builder'."
    )

    # Vérification du stage runtime
    assert "AS runtime" in content, (
        "Le Dockerfile ne contient pas de stage 'runtime'. "
        "Le second stage doit être nommé 'AS runtime' pour produire l'image finale."
    )

    # Vérification de la copie inter-stages (--from=builder)
    assert "--from=builder" in content, (
        "Le Dockerfile ne contient pas d'instruction 'COPY --from=builder'. "
        "Le stage runtime doit copier le .venv compilé depuis le stage builder."
    )


def test_dockerfile_installs_only_production_deps() -> None:
    """Vérifie que le stage builder n'installe que les dépendances de production.

    La commande 'poetry install --only main' garantit que les outils de
    développement (pytest, ruff, mypy) ne sont pas embarqués dans l'image
    finale, réduisant ainsi le poids et la surface d'attaque.
    """
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert "--only main" in content, (
        "Le Dockerfile n'utilise pas '--only main' dans la commande poetry install. "
        "Les dépendances de développement ne doivent pas être installées en production."
    )


def test_dockerfile_exposes_port_8000() -> None:
    """Vérifie que le Dockerfile expose le port 8000 (port standard du microservice FastAPI)."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert "EXPOSE 8000" in content, (
        "Le Dockerfile ne contient pas l'instruction 'EXPOSE 8000'. "
        "Le port du serveur Uvicorn doit être documenté via EXPOSE."
    )


def test_dockerfile_uses_uvicorn_cmd() -> None:
    """Vérifie que le Dockerfile lance Uvicorn comme commande de démarrage."""
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert "uvicorn" in content, (
        "Le Dockerfile ne référence pas 'uvicorn' dans la commande de démarrage. "
        "Le serveur ASGI Uvicorn doit être la commande d'entrée du conteneur."
    )
    assert "src.main:app" in content, (
        "Le Dockerfile ne pointe pas vers 'src.main:app' dans la commande CMD. "
        "Uvicorn doit cibler le point d'entrée FastAPI de l'application."
    )


def test_dockerfile_sets_python_env_vars() -> None:
    """Vérifie la présence des variables d'environnement Python recommandées.

    - PYTHONDONTWRITEBYTECODE : Évite la génération de fichiers .pyc inutiles.
    - PYTHONUNBUFFERED : Garantit l'affichage immédiat des logs dans Docker.
    """
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert "PYTHONDONTWRITEBYTECODE" in content, (
        "Le Dockerfile ne définit pas PYTHONDONTWRITEBYTECODE. "
        "Cette variable empêche la création de fichiers .pyc inutiles en conteneur."
    )
    assert "PYTHONUNBUFFERED" in content, (
        "Le Dockerfile ne définit pas PYTHONUNBUFFERED. "
        "Cette variable force les logs Python en temps réel dans les orchestrateurs."
    )


def test_dockerignore_exists() -> None:
    """Vérifie la présence du fichier .dockerignore pour optimiser le contexte de build.

    Sans .dockerignore, Docker envoie tous les fichiers du répertoire au démon,
    y compris .venv (potentiellement des centaines de Mo), .git, les caches, etc.
    """
    dockerignore = PROJECT_DIR / ".dockerignore"
    assert dockerignore.exists(), (
        "Le fichier '.dockerignore' est introuvable. "
        "Il doit exclure .venv, .git, tests/, dashboard/ et les caches du contexte de build."
    )


def test_dockerignore_excludes_dev_artifacts() -> None:
    """Vérifie que .dockerignore exclut bien les artefacts de développement."""
    dockerignore = PROJECT_DIR / ".dockerignore"
    content = dockerignore.read_text(encoding="utf-8")

    # Liste des exclusions critiques attendues
    expected_exclusions = [".venv", ".git", "tests/", "dashboard/", "__pycache__"]
    for exclusion in expected_exclusions:
        assert exclusion in content, (
            f"Le fichier .dockerignore ne contient pas l'exclusion '{exclusion}'. "
            f"Ce répertoire ou fichier ne doit pas être inclus dans le contexte de build Docker."
        )


# ==============================================================================
# Tests de Sécurisation Non-root (Hardening) — Étape 5.2
# ==============================================================================
# Ces tests valident que le Dockerfile applique le principe de moindre privilège
# en exécutant l'application sous un utilisateur non-root (appuser, UID 1000).
# ==============================================================================


def test_dockerfile_creates_non_root_user() -> None:
    """Vérifie que le Dockerfile crée un utilisateur et un groupe système non-root.

    La sécurisation non-root nécessite la création d'un groupe système
    ('appgroup') et d'un utilisateur système ('appuser') avec un UID fixe
    de 1000. L'UID fixe garantit la compatibilité avec les politiques de
    sécurité Kubernetes (PodSecurityPolicy, SecurityContext).
    """
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    # Vérification de la création du groupe système
    assert "addgroup" in content and "appgroup" in content, (
        "Le Dockerfile ne crée pas le groupe système 'appgroup'. "
        "Un groupe dédié est nécessaire pour isoler les permissions de l'application."
    )

    # Vérification de la création de l'utilisateur système avec UID 1000
    assert "adduser" in content and "appuser" in content, (
        "Le Dockerfile ne crée pas l'utilisateur système 'appuser'. "
        "Un utilisateur non-root est requis pour le principe de moindre privilège."
    )
    assert "1000" in content, (
        "Le Dockerfile ne fixe pas l'UID à 1000 pour 'appuser'. "
        "Un UID fixe est requis pour la compatibilité avec les orchestrateurs."
    )


def test_dockerfile_uses_user_directive() -> None:
    """Vérifie que le Dockerfile contient la directive USER pour basculer l'identité.

    La directive 'USER appuser' est le verrou final du hardening : elle garantit
    que la commande CMD (uvicorn) s'exécutera sous l'identité de 'appuser'
    et non sous 'root'.
    """
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert "USER appuser" in content, (
        "Le Dockerfile ne contient pas la directive 'USER appuser'. "
        "Sans cette directive, le conteneur s'exécutera en tant que root, "
        "ce qui constitue une faille de sécurité majeure."
    )


def test_dockerfile_uses_chown_on_copy() -> None:
    """Vérifie que les instructions COPY utilisent --chown pour transférer la propriété.

    Sans le flag --chown, les fichiers copiés appartiendraient à root et
    l'utilisateur appuser ne pourrait pas les lire ou les exécuter.
    Le flag --chown est préféré à un 'RUN chown -R' séparé car il évite
    de créer une couche Docker supplémentaire.
    """
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    assert "--chown=appuser:appgroup" in content, (
        "Le Dockerfile n'utilise pas '--chown=appuser:appgroup' dans les "
        "instructions COPY. Les fichiers copiés doivent appartenir à appuser "
        "pour qu'il puisse les exécuter."
    )


def test_dockerfile_user_after_copy() -> None:
    """Vérifie que la directive USER est placée APRÈS les instructions COPY.

    L'ordre est critique : les fichiers doivent être copiés (en tant que root)
    puis la propriété transférée via --chown AVANT de basculer vers appuser.
    Si USER était placé avant COPY, les opérations de copie pourraient échouer
    faute de permissions suffisantes.
    """
    dockerfile = PROJECT_DIR / "Dockerfile"
    content = dockerfile.read_text(encoding="utf-8")

    # Trouver les positions relatives de la dernière instruction COPY et de USER
    last_copy_pos = content.rfind("COPY --from=builder")
    user_pos = content.find("USER appuser")

    assert last_copy_pos != -1 and user_pos != -1, (
        "Le Dockerfile ne contient pas les instructions COPY --from=builder "
        "et USER appuser nécessaires au hardening non-root."
    )
    assert user_pos > last_copy_pos, (
        "La directive 'USER appuser' doit être placée APRÈS les instructions "
        "'COPY --from=builder' pour garantir que les fichiers sont copiés "
        "avant le basculement d'identité."
    )

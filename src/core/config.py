# ==============================================================================
# AIPE Framework - Core Configuration
# ==============================================================================
# Ce module centralise les paramètres de configuration globale de l'application.
# Conformément aux principes de la méthodologie "Twelve-Factor App", la configuration
# est lue depuis les variables d'environnement, avec des valeurs par défaut pour
# le développement local.
# ==============================================================================

import os


class Settings:
    """
    Configuration de l'application FastAPI.

    Pour un dev junior :
    - Utiliser 'os.getenv' permet d'injecter dynamiquement des variables d'environnement
      sans modifier une seule ligne de code. Par exemple, lors du déploiement Docker
      ou sur un orchestrateur (Kubernetes, Cloud Run), nous pourrons injecter
      AIPE_ENV="production" pour écraser la valeur par défaut locale.
    """

    # Titre et description de l'API exposée sur Swagger
    TITLE: str = os.getenv("AIPE_API_TITLE", "AIPE_Framework API")
    DESCRIPTION: str = os.getenv(
        "AIPE_API_DESCRIPTION",
        "Microservice d'API de production pour le Blueprint AIPE, structuré de façon modulaire.",
    )

    # Version sémantique du service
    VERSION: str = os.getenv("AIPE_API_VERSION", "0.1.0")

    # Environnement d'exécution (development, staging, production)
    ENVIRONMENT: str = os.getenv("AIPE_ENV", "development")

    # Statut opérationnel standard renvoyé par la sonde
    HEALTH_STATUS: str = os.getenv("AIPE_HEALTH_STATUS", "healthy")


# Instance globale partagée des réglages de l'application
settings = Settings()

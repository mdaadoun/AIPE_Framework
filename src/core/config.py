# ==============================================================================
# AIPE Framework - Core Configuration / Configuration Globale Core
# ==============================================================================
# This module centralizes global application settings.
# In compliance with Twelve-Factor App principles, settings are loaded
# from environment variables with local development fallbacks.
#
# Ce module centralise les paramètres de configuration globale de l'application.
# Conformément aux principes de la méthodologie "Twelve-Factor App", la configuration
# est lue depuis les variables d'environnement, avec des valeurs par défaut pour
# le développement local.
# ==============================================================================

import os


class Settings:
    """
    FastAPI application configuration / Configuration de l'application FastAPI.

    - EN: Using 'os.getenv' allows dynamically injecting environment variables
      without altering code. For instance, in Docker or orchestrator deployments
      (Kubernetes, Cloud Run), we can inject AIPE_ENV="production" to override local defaults.
    - FR: Utiliser 'os.getenv' permet d'injecter dynamiquement des variables d'environnement
      sans modifier une seule ligne de code. Par exemple, lors du déploiement Docker
      ou sur un orchestrateur (Kubernetes, Cloud Run), nous pourrons injecter
      AIPE_ENV="production" pour écraser la valeur par défaut locale.
    """

    # API Title & Description exposed on Swagger / Titre et description de l'API exposée sur Swagger
    TITLE: str = os.getenv("AIPE_API_TITLE", "AIPE_Framework API")
    DESCRIPTION: str = os.getenv(
        "AIPE_API_DESCRIPTION",
        "Microservice d'API de production pour le Blueprint AIPE, structuré de façon modulaire.",
    )

    # Service Semantic Version / Version sémantique du service
    VERSION: str = os.getenv("AIPE_API_VERSION", "0.1.0")

    # Execution Environment / Environnement d'exécution (development, staging, production)
    ENVIRONMENT: str = os.getenv("AIPE_ENV", "development")

    # Standard Operational Health Status / Statut opérationnel standard renvoyé par la sonde
    HEALTH_STATUS: str = os.getenv("AIPE_HEALTH_STATUS", "healthy")


# Shared global application settings instance / Instance globale partagée des réglages de l'application
settings = Settings()

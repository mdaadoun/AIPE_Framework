# ==============================================================================
# AIPE Framework - Pydantic Schemas - Health / Schémas Pydantic Santé
# ==============================================================================
# This module defines data validation and serialization for the Health endpoint using Pydantic.
#
# Ce module définit la validation et la sérialisation des données pour l'endpoint
# de santé de l'application à l'aide de Pydantic.
# ==============================================================================

from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    """
    Pydantic validation schema for Healthcheck response / Schéma de validation Pydantic pour la réponse Healthcheck.

    EN:
    1. Validation: Ensures returned types match expected types (e.g. str).
    2. Serialization: Parses Python objects into JSON data structures.
    3. Documentation: Automatically generates Swagger OpenAPI docs (/docs).

    FR:
    1. Validation : Vérifie que les types correspondent aux attentes (ex: str).
    2. Sérialisation : Convertit les objets Python en JSON.
    3. Documentation : Génère la doc Swagger (/docs).
    """

    status: str = Field(
        ...,
        description="Le statut opérationnel du service. Doit valoir 'healthy' si tout fonctionne.",
        examples=["healthy"],
    )
    environment: str = Field(
        ...,
        description="L'environnement d'exécution de l'API (ex: development, production).",
        examples=["development"],
    )
    version: str = Field(
        ...,
        description="La version sémantique actuelle de l'application.",
        examples=["0.1.0"],
    )

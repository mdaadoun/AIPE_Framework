# ==============================================================================
# AIPE Framework - Pydantic Schemas - Health
# ==============================================================================
# Ce module définit la validation et la sérialisation des données pour l'endpoint
# de santé de l'application à l'aide de Pydantic.
# ==============================================================================

from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    """
    Schéma de validation Pydantic pour la réponse de l'endpoint Healthcheck.

    - Un "schema" ou "model" définit la structure attendue des données (leurs clés et leurs types).
    - Pydantic effectue deux tâches majeures à l'exécution :
      1. Validation : Si les types ne correspondent pas (ex: un int là où on attend un str),
         il lève une erreur automatiquement avant que l'API ne renvoie du code erroné.
      2. Sérialisation (parsing) : Il convertit les objets Python complexes en formats
         standards de transit comme le JSON.
      3. Documentation : Ce schéma est lu par FastAPI pour générer la documentation Swagger (/docs).
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

from fastapi import FastAPI
from pydantic import BaseModel

# Initialisation de l'application FastAPI.
# FastAPI est un framework web moderne et ultra-rapide (haute performance) basé sur ASGI,
# conçu pour concevoir des API de production robustes et documentées en Python.
app = FastAPI(
    title="AIPE_Framework API",
    description="Microservice d'API de production minimal pour le Blueprint AIPE.",
    version="0.1.0",
)


# Définition du schéma de la réponse du Healthcheck via Pydantic.
# Pydantic valide automatiquement les données d'entrée/sortie à l'exécution et génère
# les schémas JSON correspondants pour la documentation interactive OpenAPI (/docs).
class HealthCheckResponse(BaseModel):
    status: str
    environment: str
    version: str


@app.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Healthcheck opérationnel",
    description="Vérifie l'état opérationnel du service. Utilisé par les orchestrateurs (Kubernetes, AWS ECS) pour monitorer et valider la disponibilité de l'application.",
)
async def health_check() -> HealthCheckResponse:
    """Retourne les métadonnées de santé de l'API."""
    # En production, ces données peuvent être issues de variables d'environnement (ex: dev, production)
    return HealthCheckResponse(
        status="OK",
        environment="production",
        version="0.1.0",
    )

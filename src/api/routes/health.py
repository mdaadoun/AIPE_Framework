# ==============================================================================
# AIPE Framework - API Routes - Health Route / Route de Santé
# ==============================================================================
# This module defines the operational health surveillance route using APIRouter.
#
# Ce module définit la route de surveillance et de santé opérationnelle.
# Il utilise un routeur dédié (APIRouter) pour isoler les routes de façon modulaire.
# ==============================================================================

from fastapi import APIRouter

from src.core.config import settings
from src.schemas.health import HealthCheckResponse

# APIRouter isolates endpoint definitions into dedicated submodules / Un APIRouter permet de découper les routes en différents fichiers.
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Healthcheck opérationnel du microservice",
    description="Vérifie l'état de fonctionnement de l'API. Cette route est exploitée par les orchestrateurs de conteneurs (Docker, Kubernetes) ou par la supervision pour s'assurer que le service répond correctement.",
)
async def health_check() -> HealthCheckResponse:
    """
    Returns API health metadata asynchronously / Retourne les métadonnées de santé de l'API de façon asynchrone.

    EN:
    - 'async def': Asynchronous functions allow the ASGI server (Uvicorn) to handle thousands of concurrent requests without blocking.
    - 'response_model': FastAPI validates that the returned dictionary matches 100% the Pydantic schema 'HealthCheckResponse'.

    FR:
    - 'async def' : En utilisant des fonctions asynchrones, FastAPI n'attend pas passivement la fin d'une requête pour en traiter une autre.
    - 'response_model' : FastAPI va forcer et valider que le dictionnaire renvoyé respecte à 100% la structure du schéma Pydantic 'HealthCheckResponse'.
    """
    return HealthCheckResponse(
        status=settings.HEALTH_STATUS,
        environment=settings.ENVIRONMENT,
        version=settings.VERSION,
    )

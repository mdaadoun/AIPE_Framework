# ==============================================================================
# AIPE Framework - API Routes - Health Route
# ==============================================================================
# Ce module définit la route de surveillance et de santé opérationnelle.
# Il utilise un routeur dédié (APIRouter) pour isoler les routes de façon modulaire.
# ==============================================================================

from fastapi import APIRouter

from src.core.config import settings
from src.schemas.health import HealthCheckResponse

# Un APIRouter permet de découper les routes de notre API en différents fichiers.
# Au lieu d'écrire toutes les routes sur l'objet 'app' global dans main.py,
# nous déclarons un sous-routeur ici et nous l'inclurons dans main.py.
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Healthcheck opérationnel du microservice",
    description="Vérifie l'état de fonctionnement de l'API. Cette route est exploitée par les orchestrateurs de conteneurs (Docker, Kubernetes) ou par la supervision pour s'assurer que le service répond correctement.",
)
async def health_check() -> HealthCheckResponse:
    """
    Retourne les métadonnées de santé de l'API de façon asynchrone.

    - 'async def' : En utilisant des fonctions asynchrones, FastAPI n'attend pas passivement
      la fin d'une requête pour en traiter une autre. Cela permet à notre serveur ASGI
      (Uvicorn) de gérer des milliers de requêtes de façon hautement concurrente.
    - 'response_model' : FastAPI va forcer et valider que le dictionnaire renvoyé
      ci-dessous respecte à 100% la structure de notre schéma Pydantic 'HealthCheckResponse'.
    """
    return HealthCheckResponse(
        status=settings.HEALTH_STATUS,
        environment=settings.ENVIRONMENT,
        version=settings.VERSION,
    )

from fastapi import APIRouter

from src.core.config import settings
from src.schemas.health import HealthCheckResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Microservice operational healthcheck",
    description="Checks API operational health status for container orchestrators and supervision probes.",
)
async def health_check() -> HealthCheckResponse:
    """Async handler returning API operational health metadata."""
    return HealthCheckResponse(
        status=settings.HEALTH_STATUS,
        environment=settings.ENVIRONMENT,
        version=settings.VERSION,
    )

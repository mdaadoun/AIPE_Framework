from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    """Pydantic schema for Healthcheck response validation and OpenAPI documentation."""

    status: str = Field(
        ...,
        description="Operational status of the service (e.g. 'healthy').",
        examples=["healthy"],
    )
    environment: str = Field(
        ...,
        description="Active runtime environment (e.g. 'development', 'production').",
        examples=["development"],
    )
    version: str = Field(
        ...,
        description="Current semantic version of the application.",
        examples=["0.1.0"],
    )

from fastapi import FastAPI

from src.api.routes import health
from src.core.config import settings

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)

# Attach modular routers
app.include_router(health.router)

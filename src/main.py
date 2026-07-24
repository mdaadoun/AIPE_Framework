# ==============================================================================
# AIPE Framework - Entry Point / Initialisation de l'API
# ==============================================================================
# Ce module est le point d'entrée principal de l'application de production.
# Il charge la configuration, configure l'application FastAPI globale et y attache
# les différents routeurs de fonctionnalités.
# ==============================================================================

from fastapi import FastAPI

from src.api.routes import health
from src.core.config import settings

# Initialisation de l'application FastAPI.
#
# - 'FastAPI' est la classe principale représentant notre serveur web d'API.
# - Nous lui passons des métadonnées issues de notre module centralisé de configuration.
# - La documentation OpenAPI interactive est automatiquement générée et exposée
#   sur les chemins '/docs' (Swagger) et '/redoc'.
app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)

# Inclusion des routeurs modulaires.
#
# Nous attachons ici le routeur de santé (/health) que nous avons défini dans son
# propre sous-module. Cela permet de garder main.py léger, lisible et propre.
# Plus tard, si nous créons d'autres fonctionnalités (ex: routes RAG, agents, LLM),
# nous créerons d'autres routeurs que nous inclurons ici avec app.include_router().
app.include_router(health.router)

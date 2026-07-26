# ==============================================================================
# AIPE Framework - Entry Point & API Initialization / Point d'Entrée & Initialisation de l'API
# ==============================================================================
# This module is the main entry point of the production application.
# It loads configuration settings, sets up the global FastAPI app, and attaches feature routers.
#
# Ce module est le point d'entrée principal de l'application de production.
# Il charge la configuration, configure l'application FastAPI globale et y attache
# les différents routeurs de fonctionnalités.
# ==============================================================================

from fastapi import FastAPI

from src.api.routes import health
from src.core.config import settings

# FastAPI application initialization / Initialisation de l'application FastAPI.
#
# EN:
# - 'FastAPI' is the core web framework class representing our API server.
# - We inject metadata from our centralized configuration module.
# - Interactive OpenAPI documentation is automatically generated at '/docs' (Swagger) and '/redoc'.
#
# FR:
# - 'FastAPI' est la classe principale représentant notre serveur web d'API.
# - Nous lui passons des métadonnées issues de notre module centralisé de configuration.
# - La documentation OpenAPI interactive est automatiquement générée et exposée
#   sur les chemins '/docs' (Swagger) et '/redoc'.
app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)

# Modular Routers Inclusion / Inclusion des routeurs modulaires.
#
# EN:
# We attach here the health router (/health) defined in its dedicated submodule.
# This keeps main.py lightweight, readable, and clean. Future features (e.g. RAG, agents, LLMs)
# will be attached using app.include_router().
#
# FR:
# Nous attachons ici le routeur de santé (/health) que nous avons défini dans son
# propre sous-module. Cela permet de garder main.py léger, lisible et propre.
# Plus tard, si nous créons d'autres fonctionnalités (ex: routes RAG, agents, LLM),
# nous créerons d'autres routeurs que nous inclurons ici avec app.include_router().
app.include_router(health.router)

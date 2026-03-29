"""
FastAPI application factory for PathFinder.

Wires together:
  - CORS middleware (wildcard by default, configurable via CORS_ORIGINS env var)
  - Request-ID / timing middleware
  - Custom exception handlers for Pydantic validation & runtime errors
  - All route modules (health, roadmap, jobs, graph)
"""
from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.middleware import add_request_id_middleware
from api.routes import graph, health, jobs, roadmap

APP_VERSION   = "1.0.0"
APP_TITLE     = "PathFinder API"
APP_DESC      = (
    "**PathFinder** — a constraint-aware, curriculum-grounded, neuro-symbolic "
    "Generative AI system for personalised DSA learning roadmaps.\n\n"
    "Combines LLM reasoning (Groq / LLaMA-3), RAG retrieval (ChromaDB), "
    "and a symbolic prerequisite dependency graph."
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀  PathFinder API starting up  |  version", APP_VERSION)
    yield
    print("🛑  PathFinder API shutting down")


def create_app() -> FastAPI:
    app = FastAPI(
        title=APP_TITLE,
        description=APP_DESC,
        version=APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ── CORS ─────────────────────────────────────────────────────────────────
    raw_origins = os.getenv("CORS_ORIGINS", "*")
    allowed_origins = [o.strip() for o in raw_origins.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Custom middleware ─────────────────────────────────────────────────────
    add_request_id_middleware(app)

    # ── Global exception handlers ─────────────────────────────────────────────
    @app.exception_handler(RuntimeError)
    async def runtime_error_handler(request: Request, exc: RuntimeError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": str(exc), "message": "Service unavailable"},
        )

    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc), "message": "Internal server error"},
        )

    # ── Routers ───────────────────────────────────────────────────────────────
    app.include_router(health.router)
    app.include_router(roadmap.router)
    app.include_router(jobs.router)
    app.include_router(graph.router)

    return app


# Module-level instance (imported by uvicorn: "api.app:app")
app = create_app()

"""
Health check endpoints.

GET /health        — lightweight liveness (no external calls)
GET /health/detail — readiness: pings LLM + queries ChromaDB collection count
"""
from __future__ import annotations

import asyncio

from fastapi import APIRouter

from api.models.responses import HealthDetailResponse, HealthResponse

APP_VERSION = "1.0.0"

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse, summary="Liveness check")
async def health() -> HealthResponse:
    """Returns 200 immediately — confirms the API process is running."""
    return HealthResponse(status="ok", version=APP_VERSION)


@router.get(
    "/detail",
    response_model=HealthDetailResponse,
    summary="Readiness check (LLM + ChromaDB)",
)
async def health_detail() -> HealthDetailResponse:
    """
    Checks external dependency health:
    - **LLM**: sends a minimal ping request to Groq
    - **ChromaDB**: verifies the collection exists and returns doc count
    """
    # ── LLM ping ──────────────────────────────────────────────────────────
    llm_status = "ok"
    try:
        from llm.client import chat  # noqa: PLC0415
        await asyncio.to_thread(
            chat, [{"role": "user", "content": "ping"}]
        )
    except Exception as exc:
        llm_status = f"error: {str(exc)[:120]}"

    # ── ChromaDB check ─────────────────────────────────────────────────────
    chromadb_status = "ok"
    chromadb_count: int | None = None
    try:
        from agents.rag_retriever import _get_collection  # noqa: PLC0415
        col = await asyncio.to_thread(_get_collection)
        chromadb_count = col.count()
    except Exception as exc:
        chromadb_status = f"error: {str(exc)[:120]}"

    overall = "ok" if llm_status == "ok" and chromadb_status == "ok" else "degraded"

    return HealthDetailResponse(
        status=overall,
        version=APP_VERSION,
        llm=llm_status,
        chromadb=chromadb_status,
        chromadb_count=chromadb_count,
    )

"""
Custom ASGI middleware for PathFinder API.

Attaches two response headers to every request:
  X-Request-Id   — unique UUID per request (useful for log correlation)
  X-Process-Time — wall-clock latency in milliseconds
"""
from __future__ import annotations

import time
import uuid

from fastapi import FastAPI, Request


def add_request_id_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def _middleware(request: Request, call_next):
        request_id = str(uuid.uuid4())
        start = time.perf_counter()

        response = await call_next(request)

        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        response.headers["X-Request-Id"]   = request_id
        response.headers["X-Process-Time"] = f"{elapsed_ms}ms"
        return response

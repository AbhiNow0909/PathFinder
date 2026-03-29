"""Tests for POST /roadmap (sync), POST /roadmap/stream (SSE), POST /roadmap/async."""
from __future__ import annotations

import json
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.tests.conftest import MOCK_ROADMAP, VALID_PAYLOAD


# ── Sync endpoint ─────────────────────────────────────────────────────────────

def test_sync_returns_roadmap(client: TestClient):
    with patch("api.routes.roadmap.run_pipeline_sync", return_value=MOCK_ROADMAP):
        response = client.post("/roadmap", json=VALID_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert "roadmap" in data
    assert data["total_time"] == 7.0
    assert data["validation_attempts"] == 1
    assert len(data["roadmap"]) == 2


def test_sync_invalid_skill_level(client: TestClient):
    bad = dict(VALID_PAYLOAD)
    bad["snapshot"] = {**VALID_PAYLOAD["snapshot"], "trees": "terrible"}
    response = client.post("/roadmap", json=bad)
    assert response.status_code == 422


def test_sync_negative_time(client: TestClient):
    bad = dict(VALID_PAYLOAD)
    bad["snapshot"] = {**VALID_PAYLOAD["snapshot"], "time_available_hours": -5}
    response = client.post("/roadmap", json=bad)
    assert response.status_code == 422


def test_sync_max_retries_out_of_range(client: TestClient):
    bad = {**VALID_PAYLOAD, "max_retries": 10}
    response = client.post("/roadmap", json=bad)
    assert response.status_code == 422


# ── SSE streaming endpoint ────────────────────────────────────────────────────

def test_stream_returns_event_stream_content_type(client: TestClient):
    """Validate the Content-Type header without running the real pipeline."""
    import asyncio

    async def fake_stream(snapshot, max_retries, queue):
        queue.put_nowait({"type": "complete", "step": 6, "total_steps": 6,
                          "result": MOCK_ROADMAP.model_dump()})
        queue.put_nowait(None)

    with patch("api.routes.roadmap.stream_pipeline", new=fake_stream):
        with client.stream("POST", "/roadmap/stream", json=VALID_PAYLOAD) as r:
            assert "text/event-stream" in r.headers["content-type"]
            lines = []
            for line in r.iter_lines():
                lines.append(line)
                if line.startswith("data:"):
                    payload = json.loads(line[len("data:"):].strip())
                    if payload.get("type") == "complete":
                        break
    assert any(l.startswith("data:") for l in lines)


# ── Async job endpoint ────────────────────────────────────────────────────────

def test_async_job_accepted(client: TestClient):
    from unittest.mock import AsyncMock
    with patch("api.routes.roadmap.run_pipeline_for_job", new_callable=AsyncMock):
        response = client.post("/roadmap/async", json=VALID_PAYLOAD)
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "pending"

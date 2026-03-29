"""Tests for /jobs endpoints (list, poll, delete)."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from api.tests.conftest import VALID_PAYLOAD


def _submit_job(client: TestClient) -> str:
    """Helper: submit an async job and return the job_id."""
    with patch("api.routes.roadmap.run_pipeline_for_job", new_callable=AsyncMock):
        response = client.post("/roadmap/async", json=VALID_PAYLOAD)
    assert response.status_code == 202
    return response.json()["job_id"]


def test_poll_job_pending(client: TestClient):
    job_id = _submit_job(client)
    poll = client.get(f"/jobs/{job_id}")
    assert poll.status_code == 200
    data = poll.json()
    assert data["job_id"] == job_id
    assert data["status"] in ("pending", "running", "done", "failed")


def test_poll_job_not_found(client: TestClient):
    response = client.get("/jobs/nonexistent-uuid-1234")
    assert response.status_code == 404


def test_delete_job_removes_it(client: TestClient):
    job_id = _submit_job(client)
    delete_resp = client.delete(f"/jobs/{job_id}")
    assert delete_resp.status_code == 204
    # Verify it's gone
    poll = client.get(f"/jobs/{job_id}")
    assert poll.status_code == 404


def test_delete_job_not_found(client: TestClient):
    response = client.delete("/jobs/ghost-id")
    assert response.status_code == 404


def test_list_jobs_returns_list(client: TestClient):
    response = client.get("/jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

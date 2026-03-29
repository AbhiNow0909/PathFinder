"""Tests for GET /health and GET /health/detail."""
from fastapi.testclient import TestClient


def test_liveness_returns_200(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_liveness_has_tracing_headers(client: TestClient):
    response = client.get("/health")
    assert "x-request-id" in response.headers
    assert "x-process-time" in response.headers


def test_liveness_request_ids_are_unique(client: TestClient):
    r1 = client.get("/health")
    r2 = client.get("/health")
    assert r1.headers["x-request-id"] != r2.headers["x-request-id"]

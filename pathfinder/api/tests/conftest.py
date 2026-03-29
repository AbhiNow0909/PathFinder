"""Shared pytest fixtures for the API test suite."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.models.responses import RoadmapResponse
from schemas.models import RoadmapStep

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture(scope="session")
def client(app):
    return TestClient(app)


# ── Shared mock data ──────────────────────────────────────────────────────────

VALID_SNAPSHOT = {
    "trees": "weak",
    "dp": "very weak",
    "arrays": "strong",
    "graphs": "medium",
    "recursion": "medium",
    "binary_search": "medium",
    "sorting": "strong",
    "time_available_hours": 20,
}

VALID_PAYLOAD = {"snapshot": VALID_SNAPSHOT, "max_retries": 3}

MOCK_ROADMAP = RoadmapResponse(
    roadmap=[
        RoadmapStep(
            step=1,
            topic="recursion",
            time_estimate_hours=2.0,
            reason="Prerequisite for Trees and Dynamic Programming.",
            reference="CLRS Chapter 4",
        ),
        RoadmapStep(
            step=2,
            topic="dynamic_programming",
            time_estimate_hours=5.0,
            reason="Core weak area — needs focused study.",
            reference="CLRS Chapter 15",
        ),
    ],
    total_time=7.0,
    skill_summary="Focus on DP and Trees. You have a solid foundation in Arrays.",
    topics_skipped=[],
    validation_attempts=1,
)

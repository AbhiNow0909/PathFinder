"""Tests for GET /graph/topics and GET /graph/concepts."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

MOCK_GRAPH = {
    "recursion":           [],
    "arrays":              [],
    "trees":               ["recursion"],
    "dynamic_programming": ["recursion", "arrays"],
    "graphs":              [],
}


def test_get_topics_returns_graph(client: TestClient):
    with patch("api.routes.graph.load_concept_graph", return_value=MOCK_GRAPH):
        response = client.get("/graph/topics")
    assert response.status_code == 200
    data = response.json()
    assert data["total_topics"] == len(MOCK_GRAPH)
    assert "recursion" in data["graph"]
    assert data["graph"]["trees"] == ["recursion"]


def test_get_concepts_returns_list(client: TestClient, tmp_path: Path):
    concepts = ["recursion", "trees", "arrays", "dynamic_programming"]
    (tmp_path / "allowed_concepts.json").write_text(json.dumps(concepts), encoding="utf-8")

    with patch("api.routes.graph._GRAPH_DIR", tmp_path):
        response = client.get("/graph/concepts")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == len(concepts)
    assert set(data["concepts"]) == set(concepts)


def test_get_concepts_missing_file(client: TestClient, tmp_path: Path):
    # Don't create the file — expect 404
    with patch("api.routes.graph._GRAPH_DIR", tmp_path):
        response = client.get("/graph/concepts")
    assert response.status_code == 404

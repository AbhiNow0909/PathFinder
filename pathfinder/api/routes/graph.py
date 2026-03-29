"""
Concept graph inspection endpoints — useful for frontend visualizations.

GET /graph/topics   — returns the full concept DAG as an adjacency dict
GET /graph/concepts — returns the list of all valid canonical concept names
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from api.models.responses import GraphConceptsResponse, GraphTopicsResponse
from graph.concept_resolver import load_concept_graph

router = APIRouter(prefix="/graph", tags=["graph"])

_GRAPH_DIR = Path(__file__).resolve().parent.parent.parent / "graph"


@router.get(
    "/topics",
    response_model=GraphTopicsResponse,
    summary="Get the concept dependency graph",
)
async def get_topics() -> GraphTopicsResponse:
    """
    Returns the DSA concept dependency DAG.

    Keys are topic names; values are lists of prerequisite topic names.
    Example: `{"trees": ["recursion"], "dynamic_programming": ["recursion", "arrays"]}`
    """
    try:
        graph = await asyncio.to_thread(load_concept_graph)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load concept graph: {exc}",
        ) from exc
    return GraphTopicsResponse(graph=graph, total_topics=len(graph))


@router.get(
    "/concepts",
    response_model=GraphConceptsResponse,
    summary="Get all valid concept names",
)
async def get_concepts() -> GraphConceptsResponse:
    """
    Returns every canonical concept name the system recognises.
    """
    concepts_path = _GRAPH_DIR / "allowed_concepts.json"
    try:
        raw = await asyncio.to_thread(
            concepts_path.read_text, encoding="utf-8"
        )
        concepts: list[str] = json.loads(raw)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="allowed_concepts.json not found",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load concepts: {exc}",
        ) from exc
    return GraphConceptsResponse(concepts=concepts, total=len(concepts))

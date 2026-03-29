"""Outbound response models for PathFinder API."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from schemas.models import RoadmapStep


# ── Job status enum ───────────────────────────────────────────────────────────

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE    = "done"
    FAILED  = "failed"


# ── Roadmap ───────────────────────────────────────────────────────────────────

class RoadmapResponse(BaseModel):
    roadmap: List[RoadmapStep]
    total_time: float
    skill_summary: str
    topics_skipped: List[str]
    validation_attempts: int


# ── Jobs ──────────────────────────────────────────────────────────────────────

class JobSummary(BaseModel):
    job_id: str
    status: JobStatus
    created_at: str
    completed_at: Optional[str] = None


class JobResponse(JobSummary):
    result: Optional[RoadmapResponse] = None
    error: Optional[str] = None


# ── Health ────────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str


class HealthDetailResponse(BaseModel):
    status: str
    version: str
    llm: str
    chromadb: str
    chromadb_count: Optional[int] = None


# ── Graph ─────────────────────────────────────────────────────────────────────

class GraphTopicsResponse(BaseModel):
    graph: Dict[str, List[str]]
    total_topics: int


class GraphConceptsResponse(BaseModel):
    concepts: List[str]
    total: int

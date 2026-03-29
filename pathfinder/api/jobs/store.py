"""
In-memory job store for async roadmap generation tasks.

Thread-safe via asyncio.Lock. Jobs are stored as plain dicts and lost on
server restart (by design — stateless sessions, no persistence needed).
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from api.models.responses import JobStatus


# ── Job data class ────────────────────────────────────────────────────────────

class Job:
    __slots__ = (
        "job_id", "status", "result", "error",
        "created_at", "completed_at", "request_data",
    )

    def __init__(self, job_id: str, request_data: dict) -> None:
        self.job_id:        str            = job_id
        self.status:        JobStatus      = JobStatus.PENDING
        self.result:        Optional[Any]  = None
        self.error:         Optional[str]  = None
        self.created_at:    str            = datetime.now(timezone.utc).isoformat()
        self.completed_at:  Optional[str]  = None
        self.request_data:  dict           = request_data


# ── In-memory store ───────────────────────────────────────────────────────────

_store: Dict[str, Job] = {}
_lock  = asyncio.Lock()


async def create_job(request_data: dict) -> Job:
    job = Job(job_id=str(uuid.uuid4()), request_data=request_data)
    async with _lock:
        _store[job.job_id] = job
    return job


async def get_job(job_id: str) -> Optional[Job]:
    return _store.get(job_id)


def list_jobs() -> list[Job]:
    return list(_store.values())


async def mark_running(job_id: str) -> None:
    async with _lock:
        if job_id in _store:
            _store[job_id].status = JobStatus.RUNNING


async def mark_done(job_id: str, result: Any) -> None:
    async with _lock:
        if job_id in _store:
            j = _store[job_id]
            j.status       = JobStatus.DONE
            j.result       = result
            j.completed_at = datetime.now(timezone.utc).isoformat()


async def mark_failed(job_id: str, error: str) -> None:
    async with _lock:
        if job_id in _store:
            j = _store[job_id]
            j.status       = JobStatus.FAILED
            j.error        = error
            j.completed_at = datetime.now(timezone.utc).isoformat()


async def remove_job(job_id: str) -> bool:
    async with _lock:
        if job_id in _store:
            del _store[job_id]
            return True
        return False

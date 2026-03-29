"""
Job management endpoints.

GET    /jobs          — list all in-memory jobs
GET    /jobs/{job_id} — poll a specific job's status and result
DELETE /jobs/{job_id} — remove a completed or failed job
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from api.jobs import store as job_store
from api.models.responses import JobResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[JobResponse], summary="List all jobs")
async def list_jobs() -> list[JobResponse]:
    """Returns all in-memory jobs (cleared on server restart)."""
    return [
        JobResponse(
            job_id=j.job_id,
            status=j.status,
            created_at=j.created_at,
            completed_at=j.completed_at,
            result=j.result,
            error=j.error,
        )
        for j in job_store.list_jobs()
    ]


@router.get("/{job_id}", response_model=JobResponse, summary="Poll a job")
async def get_job(job_id: str) -> JobResponse:
    """
    Poll a background roadmap job.

    | status | meaning |
    |---|---|
    | `pending` | queued, not yet started |
    | `running` | pipeline is actively running |
    | `done`    | `result` field is populated |
    | `failed`  | `error` field is populated |
    """
    job = await job_store.get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_id}' not found",
        )
    return JobResponse(
        job_id=job.job_id,
        status=job.status,
        created_at=job.created_at,
        completed_at=job.completed_at,
        result=job.result,
        error=job.error,
    )


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a job",
)
async def delete_job(job_id: str) -> None:
    """Remove a job from the in-memory store (does not cancel running jobs)."""
    removed = await job_store.remove_job(job_id)
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_id}' not found",
        )

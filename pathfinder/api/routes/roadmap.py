"""
Roadmap generation endpoints.

POST /roadmap         — synchronous (blocks until full pipeline completes)
POST /roadmap/stream  — SSE: streams step-by-step progress events
POST /roadmap/async   — enqueues background job; poll /jobs/{id} for result
"""
from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from api.jobs import store as job_store
from api.models.requests import RoadmapRequest
from api.models.responses import JobResponse, JobStatus, RoadmapResponse
from api.services.pipeline import (
    run_pipeline_for_job,
    run_pipeline_sync,
    stream_pipeline,
)

router = APIRouter(prefix="/roadmap", tags=["roadmap"])


# ── 1. Synchronous ────────────────────────────────────────────────────────────

@router.post(
    "",
    response_model=RoadmapResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate roadmap (synchronous)",
)
async def generate_roadmap_sync(request: RoadmapRequest) -> RoadmapResponse:
    """
    Runs the full 9-step PathFinder pipeline and returns the complete roadmap.

    ⚠️ Blocks until all steps complete (~15-60 s depending on LLM latency).
    For live progress updates use `/roadmap/stream` instead.
    """
    try:
        return await asyncio.to_thread(
            run_pipeline_sync, request.snapshot, request.max_retries
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline error: {exc}",
        ) from exc


# ── 2. SSE Streaming ──────────────────────────────────────────────────────────

@router.post(
    "/stream",
    summary="Generate roadmap with SSE progress streaming",
    response_description="text/event-stream — one JSON event per pipeline stage",
)
async def generate_roadmap_stream(request: RoadmapRequest) -> StreamingResponse:
    """
    Streams pipeline progress via **Server-Sent Events (SSE)**.

    Each `data:` line is a JSON object. Event types:

    | type | when |
    |---|---|
    | `progress` | before and after each of the 6 stages |
    | `complete`  | pipeline finished — carries full `result` |
    | `error`     | unrecoverable error — carries `message`  |

    The stream closes after a `complete` or `error` event.
    """
    queue: asyncio.Queue = asyncio.Queue()

    async def event_generator():
        task = asyncio.create_task(
            stream_pipeline(request.snapshot, request.max_retries, queue)
        )
        try:
            while True:
                item = await queue.get()
                if item is None:          # sentinel — pipeline is done
                    break
                yield f"data: {json.dumps(item)}\n\n"
        except asyncio.CancelledError:
            task.cancel()
        finally:
            if not task.done():
                task.cancel()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control":    "no-cache",
            "Connection":       "keep-alive",
            "X-Accel-Buffering": "no",   # disable nginx/proxy buffering
        },
    )


# ── 3. Async background job ───────────────────────────────────────────────────

@router.post(
    "/async",
    response_model=JobResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Generate roadmap (background job)",
)
async def generate_roadmap_async(request: RoadmapRequest) -> JobResponse:
    """
    Enqueues the pipeline as a background job and returns a `job_id` immediately.

    Poll `GET /jobs/{job_id}` for status. When `status == "done"` the
    `result` field contains the full roadmap.
    """
    job = await job_store.create_job(request.model_dump(mode="json"))
    asyncio.create_task(
        run_pipeline_for_job(request.snapshot, request.max_retries, job.job_id)
    )
    return JobResponse(
        job_id=job.job_id,
        status=JobStatus.PENDING,
        created_at=job.created_at,
    )

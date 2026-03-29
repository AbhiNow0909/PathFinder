"""
Pipeline service layer for PathFinder API.

Bridges the synchronous 9-step pipeline with async FastAPI handlers.
Provides three entry points:

  • run_pipeline_sync      — blocking, returns RoadmapResponse directly.
  • stream_pipeline        — async coroutine that feeds SSE events into an
                             asyncio.Queue; run as a background Task.
  • run_pipeline_for_job   — async wrapper used by the /roadmap/async endpoint.

SSE Event schema
----------------
Progress event:
  { "type": "progress",
    "step": <int 1-6>,  "total_steps": 6,
    "name": "<stage name>",
    "status": "running" | "done" | "failed",
    "data": { ... stage-specific payload ... } }

Complete event (final):
  { "type": "complete", "step": 6, "total_steps": 6,
    "result": { ... RoadmapResponse as dict ... } }

Error event:
  { "type": "error", "message": "<exception text>" }
"""
from __future__ import annotations

import asyncio
from typing import Any, Callable, Optional

from agents.planning_agent import generate_roadmap
from agents.rag_retriever import retrieve_curriculum_context
from agents.skill_analyzer import run_skill_analyzer
from agents.topic_ordering import run_ordering_loop
from agents.validation_agent import validate_roadmap
from graph.concept_resolver import load_concept_graph
from schemas.models import StudentSnapshot

from api.models.responses import RoadmapResponse

# ── Constants ─────────────────────────────────────────────────────────────────

TOTAL_STAGES = 6   # Skill Analysis, Topic Planning, RAG, Planning, Validation, Done

EmitFn = Optional[Callable[[dict], None]]


# ── Internal helpers ──────────────────────────────────────────────────────────

def _emit(fn: EmitFn, step: int, name: str, status: str, data: Any = None) -> None:
    """Fire a structured progress event; no-op when fn is None."""
    if fn is None:
        return
    event: dict = {
        "type": "progress",
        "step": step,
        "total_steps": TOTAL_STAGES,
        "name": name,
        "status": status,
    }
    if data is not None:
        event["data"] = data
    fn(event)


# ── Core blocking pipeline ────────────────────────────────────────────────────

def _run_blocking_pipeline(
    snapshot: StudentSnapshot,
    max_retries: int,
    emit: EmitFn = None,
) -> RoadmapResponse:
    """
    Runs the full PathFinder pipeline synchronously.

    Stages:
      1  Skill Analysis        — run_skill_analyzer
      2  Topic Planning        — run_ordering_loop (steps 2-6 internally)
      3  Curriculum Retrieval  — retrieve_curriculum_context
      4  Planning Agent        — generate_roadmap  (per attempt)
      5  Validation Agent      — validate_roadmap  (per attempt)
    """

    # ── Stage 1: Skill Analysis ───────────────────────────────────────────
    _emit(emit, 1, "Skill Analysis", "running")
    skill_output = run_skill_analyzer(snapshot)
    analysis     = skill_output.analysis
    _emit(emit, 1, "Skill Analysis", "done", {
        "weak_topics":          analysis.weak_topics,
        "mastered_topics":      analysis.mastered_topics,
        "time_budget":          analysis.time_budget,
        "difficulty_tolerance": analysis.difficulty_tolerance,
        "summary":              skill_output.summary,
    })

    # ── Stage 2: Topic Planning (resolution → graph expansion → LLM loop) ──
    _emit(emit, 2, "Topic Planning", "running", {
        "info": "Resolving topics → expanding prerequisites → LLM-driven ordering",
    })
    ordering = run_ordering_loop(analysis)
    _emit(emit, 2, "Topic Planning", "done", {
        "ordered_topics":  [t.topic for t in ordering.ordered_topics],
        "topics_skipped":  ordering.topics_skipped,
        "time_allocated":  ordering.time_allocated,
        "time_budget":     ordering.time_budget,
    })

    # ── Stage 3: Curriculum Retrieval (RAG) ──────────────────────────────
    n_topics = len(ordering.ordered_topics)
    _emit(emit, 3, "Curriculum Retrieval", "running", {
        "info": f"Retrieving curriculum context for {n_topics} topics",
    })
    curriculum_entries = retrieve_curriculum_context(ordering.ordered_topics)
    _emit(emit, 3, "Curriculum Retrieval", "done", {
        "topics_retrieved": [e.concept for e in curriculum_entries],
    })

    # ── Stages 4 + 5: Planning → Validation self-correction loop ─────────
    graph          = load_concept_graph()
    attempt        = 1
    feedback: Optional[str] = None
    final_roadmap  = None
    validation_attempts = 0

    while attempt <= max(1, max_retries):
        # Stage 4 — Planning Agent
        _emit(emit, 4, "Planning Agent", "running", {
            "attempt": attempt,
            "has_feedback": feedback is not None,
        })
        final_roadmap = generate_roadmap(curriculum_entries, analysis, feedback=feedback)
        _emit(emit, 4, "Planning Agent", "done", {
            "attempt":        attempt,
            "steps_generated": len(final_roadmap.roadmap),
            "total_time":     final_roadmap.total_time,
        })

        # Stage 5 — Validation Agent
        _emit(emit, 5, "Validation", "running", {"attempt": attempt})
        errors = validate_roadmap(final_roadmap, analysis, graph)
        validation_attempts = attempt

        if not errors:
            _emit(emit, 5, "Validation", "done", {
                "attempt": attempt, "passed": True, "errors": [],
            })
            break
        else:
            _emit(emit, 5, "Validation", "done", {
                "attempt": attempt, "passed": False, "errors": errors,
            })
            feedback = "\n".join(errors)
            attempt += 1

    return RoadmapResponse(
        roadmap=final_roadmap.roadmap,
        total_time=final_roadmap.total_time,
        skill_summary=skill_output.summary,
        topics_skipped=ordering.topics_skipped,
        validation_attempts=validation_attempts,
    )


# ── 1. Sync entry point ───────────────────────────────────────────────────────

def run_pipeline_sync(
    snapshot: StudentSnapshot,
    max_retries: int = 3,
) -> RoadmapResponse:
    """Blocking pipeline — no SSE events emitted."""
    return _run_blocking_pipeline(snapshot, max_retries, emit=None)


# ── 2. SSE streaming entry point ─────────────────────────────────────────────

async def stream_pipeline(
    snapshot: StudentSnapshot,
    max_retries: int,
    queue: asyncio.Queue,
) -> None:
    """
    Runs the pipeline in a thread pool and feeds SSE events into `queue`.

    The caller should iterate the queue until it receives None (sentinel),
    which signals the pipeline has finished (success or error).
    """
    loop = asyncio.get_running_loop()

    def emit(event: dict) -> None:
        # thread-safe: schedule a put on the event loop from the worker thread
        loop.call_soon_threadsafe(queue.put_nowait, event)

    try:
        result = await asyncio.to_thread(
            _run_blocking_pipeline, snapshot, max_retries, emit
        )
        loop.call_soon_threadsafe(queue.put_nowait, {
            "type":        "complete",
            "step":        TOTAL_STAGES,
            "total_steps": TOTAL_STAGES,
            "result":      result.model_dump(),
        })
    except Exception as exc:
        loop.call_soon_threadsafe(queue.put_nowait, {
            "type":    "error",
            "message": str(exc),
        })
    finally:
        loop.call_soon_threadsafe(queue.put_nowait, None)  # sentinel


# ── 3. Async job entry point ──────────────────────────────────────────────────

async def run_pipeline_for_job(
    snapshot: StudentSnapshot,
    max_retries: int,
    job_id: str,
) -> None:
    """
    Fire-and-forget coroutine: runs the pipeline in a thread pool and
    updates the job store with the result or error when done.
    """
    from api.jobs.store import mark_done, mark_failed, mark_running  # noqa

    await mark_running(job_id)
    try:
        result = await asyncio.to_thread(
            _run_blocking_pipeline, snapshot, max_retries, None
        )
        await mark_done(job_id, result)
    except Exception as exc:
        await mark_failed(job_id, str(exc))

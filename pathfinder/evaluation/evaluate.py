"""
evaluate.py — Automated Evaluation Script for PathFinder

Runs all 3 systems (B1: LLM-only, B2: LLM+RAG, Proposed) on the 30-profile
test dataset and computes PVR, TBA, and WTC metrics for each.

Usage (from pathfinder/ directory):
    python -m evaluation.evaluate

Results are printed to console and saved to evaluation/results.json
"""

from __future__ import annotations

import json
import re
import sys
import io
import time
from pathlib import Path
from typing import Any

# Fix Windows console unicode
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Imports from project ──────────────────────────────────────────────────────

from schemas.models import StudentSnapshot, SkillAnalysis, FinalRoadmap, RoadmapStep
from agents.skill_analyzer import analyze_skills
from agents.topic_ordering import run_ordering_loop
from agents.rag_retriever import retrieve_curriculum_context
from agents.planning_agent import generate_roadmap
from agents.validation_agent import validate_roadmap
from graph.concept_resolver import (
    resolve_topics,
    expand_weak_topics,
    load_concept_graph,
)
from llm.client import chat as llm_chat

# ── Constants ─────────────────────────────────────────────────────────────────

GRAPH = load_concept_graph()
PROFILES_PATH = Path(__file__).parent / "test_profiles.json"
RESULTS_PATH  = Path(__file__).parent / "results.json"

# SkillLevel-to-numeric for the StudentSnapshot
# Maps fields that the model uses (note: linked_list, stack_queue are not in StudentSnapshot)
SNAPSHOT_FIELDS = {"trees", "dp", "arrays", "graphs", "recursion", "binary_search", "sorting"}

# Map test profile topic names → StudentSnapshot field names
PROFILE_TO_SNAPSHOT = {
    "trees": "trees",
    "dp": "dp",
    "dynamic_programming": "dp",
    "arrays": "arrays",
    "graphs": "graphs",
    "recursion": "recursion",
    "binary_search": "binary_search",
    "sorting": "sorting",
    # Fields not in StudentSnapshot — used for WTC only (not forwarded to snapshot)
    "linked_list": None,
    "stack_queue": None,
}

# ── Metric Computation ────────────────────────────────────────────────────────

def compute_pvr(roadmap: FinalRoadmap, graph: dict, mastered_topics: list[str] | None = None) -> bool:
    """
    Returns True if there is at least one prerequisite violation in the roadmap.
    A prerequisite is satisfied if it appears earlier in the roadmap OR is in mastered_topics.
    This mirrors the validation_agent logic exactly.
    """
    seen = set()
    mastered = set(mastered_topics or [])
    for step in roadmap.roadmap:
        topic = step.topic
        prereqs = graph.get(topic, [])
        for p in prereqs:
            # Satisfied if mastered or appears earlier in roadmap
            if p not in mastered and p not in seen:
                return True  # violation
        seen.add(topic)
    return False


def compute_tba(roadmap: FinalRoadmap, time_budget: float) -> bool:
    """Returns True if total_time <= time_budget (within 0.1h tolerance)."""
    return roadmap.total_time <= time_budget + 0.1


def compute_wtc(roadmap: FinalRoadmap, weak_topics: list[str]) -> float:
    """
    Weak Topic Coverage: fraction of identified weak topics covered in the roadmap.
    (0.0 – 1.0)
    """
    if not weak_topics:
        return 1.0
    roadmap_topics = {step.topic for step in roadmap.roadmap}
    covered = sum(1 for t in weak_topics if t in roadmap_topics)
    return covered / len(weak_topics)


def compute_constrained_wtc(roadmap: FinalRoadmap, weak_topics: list[str], 
                            time_budget: float, graph: dict, 
                            mastered_topics: list[str] | None = None) -> float:
    """
    Constrained Weak Topic Coverage: WTC among roadmaps that satisfy both 
    prerequisite and time budget constraints.
    
    Returns 0.0 if the roadmap has any violations (invalid roadmap).
    Returns normal WTC if the roadmap is valid.
    
    This metric penalizes systems that achieve high raw WTC by violating constraints.
    """
    pvr_violated = compute_pvr(roadmap, graph, mastered_topics)
    tba_pass = compute_tba(roadmap, time_budget)
    
    # If roadmap is invalid, constrained coverage is zero
    if pvr_violated or not tba_pass:
        return 0.0
    
    # If roadmap is valid, return normal WTC
    return compute_wtc(roadmap, weak_topics)


# ── Profile → StudentSnapshot ─────────────────────────────────────────────────

def profile_to_snapshot(profile: dict) -> StudentSnapshot:
    """
    Build a StudentSnapshot from a test profile dict.
    Only includes fields that StudentSnapshot accepts.
    Unmapped fields (linked_list, stack_queue) are dropped.
    """
    kwargs: dict[str, Any] = {}
    for topic, level in profile.items():
        if topic == "time_available_hours":
            kwargs["time_available_hours"] = level
        elif topic in SNAPSHOT_FIELDS:
            kwargs[topic] = level
        # else: silently skip (e.g. linked_list, stack_queue)
    return StudentSnapshot(**kwargs)


def get_weak_topics_from_profile(profile: dict) -> list[str]:
    """
    Returns weak topics from the profile that fall within the StudentSnapshot field
    universe (i.e., topics the system can actually reason about via the graph).
    This ensures WTC comparisons are fair across all systems.
    """
    weak = []
    for topic, level in profile.items():
        if topic == "time_available_hours":
            continue
        # Only count topics that StudentSnapshot can express
        if topic not in SNAPSHOT_FIELDS:
            continue
        if level in {"weak", "very weak"}:
            weak.append(topic)
    return weak


# ── Baseline 1: LLM-Only ─────────────────────────────────────────────────────

B1_SYSTEM_PROMPT = """You are a DSA learning coach. Generate a personalized study roadmap in JSON.

Output format (JSON only, no markdown):
{
  "roadmap": [
    {"step": 1, "topic": "<topic>", "time_estimate_hours": <float>, "reason": "<brief reason>", "reference": "N/A"}
  ],
  "total_time": <sum>
}

Rules:
- Focus on topics the student is weak in.
- Order topics in a logical learning sequence.
- Return ONLY valid JSON."""


def run_b1(profile: dict) -> FinalRoadmap:
    """Baseline 1: Direct LLM prompt, no graph, no RAG."""
    skill_items = {k: v for k, v in profile.items() if k != "time_available_hours"}
    time_budget = profile["time_available_hours"]

    user_prompt = (
        f"Student skill profile: {json.dumps(skill_items)}\n"
        f"Time budget: {time_budget} hours\n\n"
        f"Generate a learning roadmap JSON."
    )

    try:
        response = llm_chat(messages=[
            {"role": "system", "content": B1_SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ], temperature=0.4)

        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON in B1 response")
        parsed = json.loads(json_match.group())
        return FinalRoadmap(**parsed)

    except Exception as e:
        print(f"    [B1 error] {e} — returning empty roadmap")
        return FinalRoadmap(roadmap=[], total_time=0.0)


# ── Baseline 2: LLM + RAG (no graph) ─────────────────────────────────────────

B2_SYSTEM_PROMPT = """You are a DSA learning coach. You will receive curriculum content.
Generate a personalized study roadmap in JSON using the curriculum context.

Output format (JSON only):
{
  "roadmap": [
    {"step": 1, "topic": "<topic>", "time_estimate_hours": <float>, "reason": "<brief reason>", "reference": "<source>"}
  ],
  "total_time": <sum>
}

Rules:
- Focus on topics the student is weak in.
- Order topics logically based on curriculum context.
- Return ONLY valid JSON."""


def run_b2(profile: dict, analysis: SkillAnalysis) -> FinalRoadmap:
    """Baseline 2: RAG retrieval to ground LLM, but no graph constraint."""
    time_budget = profile["time_available_hours"]

    # Use the ordering loop's result to get topics, but skip graph expansion
    # by simply using weak topics in alphabetical order (no prerequisite enforcement)
    snapshot = profile_to_snapshot(profile)
    weak_topics = analysis.weak_topics  # from deterministic skill analyzer

    # Build fake OrderedTopic list from weak topics only (no graph expansion)
    from schemas.models import OrderedTopic
    time_per_topic = time_budget / max(len(weak_topics), 1)
    ordered_topics = [
        OrderedTopic(
            topic=t,
            is_target=True,
            estimated_hours=round(time_per_topic, 1),
            reason="RAG-only baseline"
        )
        for t in weak_topics
    ]

    if not ordered_topics:
        return FinalRoadmap(roadmap=[], total_time=0.0)

    # Retrieve RAG context for those topics
    try:
        entries = retrieve_curriculum_context(ordered_topics)
    except Exception as e:
        print(f"    [B2 RAG error] {e}")
        entries = []

    if not entries:
        return FinalRoadmap(roadmap=[], total_time=0.0)

    # Build curriculum payload
    context_blocks = []
    for i, entry in enumerate(entries, 1):
        block = (
            f"Step {i}: {entry.concept}\n"
            f"  Reference: {entry.reference}\n"
            f"  Context: {entry.context[:600]}...\n"
        )
        context_blocks.append(block)
    curriculum_payload = "\n\n".join(context_blocks)

    user_prompt = (
        f"Student skill profile: {json.dumps({k: v for k, v in profile.items() if k != 'time_available_hours'})}\n"
        f"Time budget: {time_budget} hours\n\n"
        f"Curriculum context:\n{curriculum_payload}\n\n"
        f"Generate the roadmap JSON."
    )

    try:
        response = llm_chat(messages=[
            {"role": "system", "content": B2_SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ], temperature=0.3)

        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON in B2 response")
        parsed = json.loads(json_match.group())
        return FinalRoadmap(**parsed)

    except Exception as e:
        print(f"    [B2 LLM error] {e} — returning empty roadmap")
        return FinalRoadmap(roadmap=[], total_time=0.0)


# ── Proposed System ───────────────────────────────────────────────────────────

def run_proposed(analysis: SkillAnalysis) -> FinalRoadmap:
    """Proposed: Graph + RAG + LLM + Validation with self-correction loop."""
    max_retries = 3
    feedback = None
    final_roadmap = None

    try:
        ordering = run_ordering_loop(analysis)
        curriculum_entries = retrieve_curriculum_context(ordering.ordered_topics)
    except Exception as e:
        print(f"    [Proposed pipeline error] {e}")
        return FinalRoadmap(roadmap=[], total_time=0.0)

    for attempt in range(1, max_retries + 1):
        try:
            final_roadmap = generate_roadmap(curriculum_entries, analysis, feedback=feedback)
            errors = validate_roadmap(final_roadmap, analysis, GRAPH)

            if not errors:
                break
            else:
                feedback = "\n".join(errors)
        except Exception as e:
            print(f"    [Proposed attempt {attempt} error] {e}")
            if final_roadmap is None:
                final_roadmap = FinalRoadmap(roadmap=[], total_time=0.0)
            break

    return final_roadmap if final_roadmap else FinalRoadmap(roadmap=[], total_time=0.0)


# ── Main Evaluation Loop ──────────────────────────────────────────────────────

def evaluate():
    print("=" * 65)
    print("PathFinder — Automated Evaluation (N=30 profiles)")
    print("=" * 65)

    with open(PROFILES_PATH, "r", encoding="utf-8") as f:
        profiles = json.load(f)

    results = []

    # Aggregate counters
    counts = {
        "b1":       {"pvr_violations": 0, "tba_pass": 0, "wtc_total": 0.0, "constrained_wtc_total": 0.0, "n": 0},
        "b2":       {"pvr_violations": 0, "tba_pass": 0, "wtc_total": 0.0, "constrained_wtc_total": 0.0, "n": 0},
        "proposed": {"pvr_violations": 0, "tba_pass": 0, "wtc_total": 0.0, "constrained_wtc_total": 0.0, "n": 0},
    }

    for i, entry in enumerate(profiles, 1):
        pid      = entry["id"]
        category = entry["category"]
        profile  = entry["profile"]
        time_budget = profile["time_available_hours"]

        print(f"\n[{i:02d}/30] Profile {pid} ({category}) — {time_budget}h budget")

        # Build snapshot + analysis (shared across all systems)
        snapshot = profile_to_snapshot(profile)
        analysis = analyze_skills(snapshot)
        weak_topics_ground_truth = get_weak_topics_from_profile(profile)

        row = {
            "id": pid,
            "category": category,
            "time_budget": time_budget,
            "weak_topics_gt": weak_topics_ground_truth,
        }

        # ── B1: LLM-Only ──────────────────────────────────────────────────
        print("  [B1] LLM-Only...", end=" ", flush=True)
        t0 = time.time()
        b1_roadmap = run_b1(profile)
        b1_pvr = compute_pvr(b1_roadmap, GRAPH, analysis.mastered_topics)
        b1_tba = compute_tba(b1_roadmap, time_budget)
        b1_wtc = compute_wtc(b1_roadmap, weak_topics_ground_truth)
        b1_constrained_wtc = compute_constrained_wtc(b1_roadmap, weak_topics_ground_truth, 
                                                      time_budget, GRAPH, analysis.mastered_topics)
        print(f"PVR={'YES' if b1_pvr else 'NO'} TBA={'PASS' if b1_tba else 'FAIL'} WTC={b1_wtc:.2f} CWTC={b1_constrained_wtc:.2f} ({time.time()-t0:.1f}s)")

        counts["b1"]["pvr_violations"] += int(b1_pvr)
        counts["b1"]["tba_pass"]       += int(b1_tba)
        counts["b1"]["wtc_total"]      += b1_wtc
        counts["b1"]["constrained_wtc_total"] += b1_constrained_wtc
        counts["b1"]["n"]              += 1

        row["b1"] = {
            "pvr_violated": b1_pvr,
            "tba_pass": b1_tba,
            "wtc": round(b1_wtc, 4),
            "constrained_wtc": round(b1_constrained_wtc, 4),
            "roadmap_topics": [s.topic for s in b1_roadmap.roadmap],
            "total_time": b1_roadmap.total_time,
        }

        # ── B2: LLM + RAG ─────────────────────────────────────────────────
        print("  [B2] LLM+RAG...", end=" ", flush=True)
        t0 = time.time()
        b2_roadmap = run_b2(profile, analysis)
        b2_pvr = compute_pvr(b2_roadmap, GRAPH, analysis.mastered_topics)
        b2_tba = compute_tba(b2_roadmap, time_budget)
        b2_wtc = compute_wtc(b2_roadmap, weak_topics_ground_truth)
        b2_constrained_wtc = compute_constrained_wtc(b2_roadmap, weak_topics_ground_truth,
                                                      time_budget, GRAPH, analysis.mastered_topics)
        print(f"PVR={'YES' if b2_pvr else 'NO'} TBA={'PASS' if b2_tba else 'FAIL'} WTC={b2_wtc:.2f} CWTC={b2_constrained_wtc:.2f} ({time.time()-t0:.1f}s)")

        counts["b2"]["pvr_violations"] += int(b2_pvr)
        counts["b2"]["tba_pass"]       += int(b2_tba)
        counts["b2"]["wtc_total"]      += b2_wtc
        counts["b2"]["constrained_wtc_total"] += b2_constrained_wtc
        counts["b2"]["n"]              += 1

        row["b2"] = {
            "pvr_violated": b2_pvr,
            "tba_pass": b2_tba,
            "wtc": round(b2_wtc, 4),
            "constrained_wtc": round(b2_constrained_wtc, 4),
            "roadmap_topics": [s.topic for s in b2_roadmap.roadmap],
            "total_time": b2_roadmap.total_time,
        }

        # ── Proposed ──────────────────────────────────────────────────────
        print("  [Proposed] Graph+RAG+LLM+Validation...", end=" ", flush=True)
        t0 = time.time()
        prop_roadmap = run_proposed(analysis)
        prop_pvr = compute_pvr(prop_roadmap, GRAPH, analysis.mastered_topics)
        prop_tba = compute_tba(prop_roadmap, time_budget)
        prop_wtc = compute_wtc(prop_roadmap, weak_topics_ground_truth)
        prop_constrained_wtc = compute_constrained_wtc(prop_roadmap, weak_topics_ground_truth,
                                                        time_budget, GRAPH, analysis.mastered_topics)
        print(f"PVR={'YES' if prop_pvr else 'NO'} TBA={'PASS' if prop_tba else 'FAIL'} WTC={prop_wtc:.2f} CWTC={prop_constrained_wtc:.2f} ({time.time()-t0:.1f}s)")

        counts["proposed"]["pvr_violations"] += int(prop_pvr)
        counts["proposed"]["tba_pass"]       += int(prop_tba)
        counts["proposed"]["wtc_total"]      += prop_wtc
        counts["proposed"]["constrained_wtc_total"] += prop_constrained_wtc
        counts["proposed"]["n"]              += 1

        row["proposed"] = {
            "pvr_violated": prop_pvr,
            "tba_pass": prop_tba,
            "wtc": round(prop_wtc, 4),
            "constrained_wtc": round(prop_constrained_wtc, 4),
            "roadmap_topics": [s.topic for s in prop_roadmap.roadmap],
            "total_time": prop_roadmap.total_time,
        }

        results.append(row)

    # ── Summary ───────────────────────────────────────────────────────────────

    N = len(profiles)
    print("\n" + "=" * 65)
    print("EVALUATION SUMMARY")
    print("=" * 65)
    print(f"{'Metric':<35} {'B1 (LLM-Only)':>14} {'B2 (LLM+RAG)':>14} {'Proposed':>14}")
    print("-" * 79)

    def fmt_pvr(c):
        return f"{c['pvr_violations'] / c['n'] * 100:.1f}%"

    def fmt_tba(c):
        return f"{c['tba_pass'] / c['n'] * 100:.1f}%"

    def fmt_wtc(c):
        return f"{c['wtc_total'] / c['n'] * 100:.1f}%"

    def fmt_cwtc(c):
        return f"{c['constrained_wtc_total'] / c['n'] * 100:.1f}%"

    print(f"{'Prereq Violation Rate (PVR) ↓':<35} {fmt_pvr(counts['b1']):>14} {fmt_pvr(counts['b2']):>14} {fmt_pvr(counts['proposed']):>14}")
    print(f"{'Time Budget Adherence (TBA) ↑':<35} {fmt_tba(counts['b1']):>14} {fmt_tba(counts['b2']):>14} {fmt_tba(counts['proposed']):>14}")
    print(f"{'Weak Topic Coverage (WTC) ↑':<35} {fmt_wtc(counts['b1']):>14} {fmt_wtc(counts['b2']):>14} {fmt_wtc(counts['proposed']):>14}")
    print(f"{'Constrained WTC (CWTC) ↑':<35} {fmt_cwtc(counts['b1']):>14} {fmt_cwtc(counts['b2']):>14} {fmt_cwtc(counts['proposed']):>14}")
    print("=" * 65)

    # Save detailed results
    output = {
        "summary": {
            "n": N,
            "b1": {
                "pvr": round(counts["b1"]["pvr_violations"] / N * 100, 1),
                "tba": round(counts["b1"]["tba_pass"] / N * 100, 1),
                "wtc": round(counts["b1"]["wtc_total"] / N * 100, 1),
                "constrained_wtc": round(counts["b1"]["constrained_wtc_total"] / N * 100, 1),
            },
            "b2": {
                "pvr": round(counts["b2"]["pvr_violations"] / N * 100, 1),
                "tba": round(counts["b2"]["tba_pass"] / N * 100, 1),
                "wtc": round(counts["b2"]["wtc_total"] / N * 100, 1),
                "constrained_wtc": round(counts["b2"]["constrained_wtc_total"] / N * 100, 1),
            },
            "proposed": {
                "pvr": round(counts["proposed"]["pvr_violations"] / N * 100, 1),
                "tba": round(counts["proposed"]["tba_pass"] / N * 100, 1),
                "wtc": round(counts["proposed"]["wtc_total"] / N * 100, 1),
                "constrained_wtc": round(counts["proposed"]["constrained_wtc_total"] / N * 100, 1),
            },
        },
        "per_profile": results,
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\nDetailed results saved to: {RESULTS_PATH}")
    print("\nCopy these values into your LaTeX Table I in paper.txt:")
    s = output["summary"]
    print(f"  B1:       PVR={s['b1']['pvr']}%  TBA={s['b1']['tba']}%  WTC={s['b1']['wtc']}%  CWTC={s['b1']['constrained_wtc']}%")
    print(f"  B2:       PVR={s['b2']['pvr']}%  TBA={s['b2']['tba']}%  WTC={s['b2']['wtc']}%  CWTC={s['b2']['constrained_wtc']}%")
    print(f"  Proposed: PVR={s['proposed']['pvr']}%  TBA={s['proposed']['tba']}%  WTC={s['proposed']['wtc']}%  CWTC={s['proposed']['constrained_wtc']}%")

    return output


if __name__ == "__main__":
    evaluate()

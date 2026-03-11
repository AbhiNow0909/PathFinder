# agents/topic_ordering.py
"""
Step 6 of the pipeline: Iterative Ordering Loop (LLM + Graph).

This replaces static topological sorting with an adaptive, LLM-driven loop.

Loop logic:
  while time remains and candidates left:
      1. Compute eligible topics (graph constraint)
      2. Compute what each eligible topic unlocks (downstream impact)
      3. LLM selects the best next topic + estimates time
      4. If time budget allows → append to roadmap, update state
      5. If time budget exceeded → skip remaining, stop

The graph constrains the search space; the LLM reasons within that space.
"""

from __future__ import annotations

import json
import re
from typing import Dict, List, Set

from llm.client import chat as llm_chat

from graph.concept_resolver import (
    expand_weak_topics,
    get_eligible_topics,
    get_unlock_map,
    load_concept_graph,
    resolve_topics,
)
from schemas.models import (
    OrderedTopic,
    OrderingResult,
    SkillAnalysis,
    SkillLevel,
)

# ── Relative difficulty weights (used to split budget proportionally) ─────────

_TOPIC_WEIGHT: Dict[str, float] = {
    "arrays": 1.0,
    "linked_list": 1.5,
    "stack_queue": 1.5,
    "two_pointers": 1.0,
    "sorting": 1.5,
    "binary_search": 1.0,
    "hashing": 1.0,
    "heap": 1.5,
    "recursion": 2.0,
    "backtracking": 2.5,
    "trees": 2.5,
    "balanced_trees": 2.5,
    "graphs": 3.0,
    "greedy": 1.5,
    "dynamic_programming": 3.5,
}

# Weaker students need more hours; stronger students less
_SKILL_MULTIPLIER: Dict[str, float] = {
    "very weak": 1.4,
    "weak": 1.2,
    "medium": 0.6,
    "strong": 0.3,
    "very strong": 0.1,
}

# Prerequisite topics only need a brush-up, not full mastery
_PREREQ_DISCOUNT = 0.5


def _estimate_hours(
    topic: str,
    remaining_topics: List[str],
    time_remaining: float,
    skill_map: Dict[str, str] | None = None,
    weak_set: Set[str] | None = None,
) -> float:
    """
    Budget-proportional time estimate: allocate time_remaining across
    remaining topics weighted by difficulty, adjusted for the student's
    skill level and whether the topic is a target or prerequisite.
    """
    weights: Dict[str, float] = {}
    for t in remaining_topics:
        w = _TOPIC_WEIGHT.get(t, 1.5)
        # Skill-level adjustment: weak students need more time
        if skill_map and t in skill_map:
            w *= _SKILL_MULTIPLIER.get(skill_map[t], 1.0)
        # PREREQ discount: student only needs enough to unlock targets
        if weak_set is not None and t not in weak_set:
            w *= _PREREQ_DISCOUNT
        weights[t] = w

    total_weight = sum(weights.values())
    if total_weight == 0:
        return max(0.5, time_remaining / max(len(remaining_topics), 1))
    share = (weights.get(topic, 1.5) / total_weight) * time_remaining
    return round(max(0.5, share), 1)

# ── LLM Topic Picker ─────────────────────────────────────────────────────────

PICKER_SYSTEM_PROMPT = """You are an expert DSA learning coach deciding the optimal next topic for a student.

You will be given:
- The student's skill profile (what they're weak/strong at)
- A list of eligible topics they can study next (all valid — prerequisites satisfied)
- For each eligible topic: whether it is a TARGET (weak area they need) or a PREREQUISITE (filler to unlock targets)
- For each eligible topic: what other topics it would UNLOCK if completed
- What they have already completed in this roadmap
- Remaining time budget in hours

Your job: Pick the ONE topic that maximizes learning impact AND estimate study hours.

Reasoning guidelines:
- TARGET topics matter more than PREREQUISITE topics — they are the student's real weak areas
- But if a PREREQUISITE unlocks multiple targets, it may be worth doing first
- Prefer topics that unlock the most downstream topics (high leverage)
- Prefer topics the student is weakest at (highest need)
- Consider building momentum — easier foundational topics before harder ones
- Estimate hours conservatively but realistically given the student's skill level on that topic
- Weaker students need more time per topic; stronger students need less

Rules:
- You MUST pick from the eligible list only. No other topics.
- estimated_hours must be a positive number (0.5 minimum).
- Return JSON only. No explanation outside the JSON.

Output format:
{
  "selected": "<topic_from_eligible_list>",
  "estimated_hours": <number>,
  "reason": "<one sentence explaining why this topic, at this position, for this student>"
}"""


def _build_topic_context(
    eligible: List[str],
    weak_set: Set[str],
    unlock_map: Dict[str, List[str]],
) -> str:
    """Build a per-topic context string showing target/prereq status and unlocks."""
    lines = []
    for topic in eligible:
        role = "TARGET (weak area)" if topic in weak_set else "PREREQUISITE (filler)"
        unlocks = unlock_map.get(topic, [])
        unlock_str = ", ".join(unlocks) if unlocks else "nothing new"
        lines.append(f"  - {topic}: {role} | unlocks → [{unlock_str}]")
    return "\n".join(lines)


def _llm_pick_next(
    eligible: List[str],
    completed: List[str],
    weak_concepts: List[str],
    skill_map: Dict[str, SkillLevel],
    difficulty_tolerance: str,
    unlock_map: Dict[str, List[str]],
    time_remaining: float,
    weak_set: Set[str] | None = None,
) -> dict:
    """
    Ask the LLM to pick the best next topic from the eligible list.
    Returns {"selected": "<topic>", "estimated_hours": float, "reason": "..."}.
    """
    weak_set = set(weak_concepts)
    topic_context = _build_topic_context(eligible, weak_set, unlock_map)

    user_prompt = (
        f"Student skill profile: {json.dumps(skill_map)}\n"
        f"Difficulty tolerance: {difficulty_tolerance}\n"
        f"Weak topics (primary targets): {weak_concepts}\n"
        f"Already completed in roadmap: {completed if completed else 'nothing yet'}\n"
        f"Remaining time budget: {time_remaining:.1f} hours\n\n"
        f"Eligible topics:\n{topic_context}\n\n"
        "Pick the best next topic, estimate hours. Return JSON only."
    )

    try:
        text = llm_chat(messages=[
            {"role": "system", "content": PICKER_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ])

        # Robust JSON extraction — handle markdown fences or extra text
        json_match = re.search(r'\{[^}]+\}', text)
        if not json_match:
            raise ValueError("No JSON object found in LLM response")
        parsed = json.loads(json_match.group())

        selected = parsed.get("selected", "")
        reason = parsed.get("reason", "")
        estimated = float(parsed.get("estimated_hours", 0))

        # Validate: LLM must pick from the eligible list
        if selected not in eligible:
            selected = eligible[0]
            reason = f"LLM picked invalid topic; defaulting to '{selected}'"

        # Clamp estimated hours to reasonable bounds
        if estimated < 0.5:
            estimated = _estimate_hours(
                selected, eligible, time_remaining,
                skill_map=skill_map, weak_set=weak_set,
            )

        return {"selected": selected, "estimated_hours": estimated, "reason": reason}

    except Exception:
        fallback = eligible[0]
        return {
            "selected": fallback,
            "estimated_hours": _estimate_hours(
                fallback, eligible, time_remaining,
                skill_map=skill_map, weak_set=weak_set,
            ),
            "reason": "LLM fallback — selected first eligible topic",
        }


# ── The Iterative Ordering Loop ──────────────────────────────────────────────


def run_ordering_loop(analysis: SkillAnalysis) -> OrderingResult:
    """
    Step 6: Iterative Ordering Loop.

    Takes the SkillAnalysis from Step 1, resolves topics, expands
    prerequisites, then iteratively asks the LLM to pick the next
    best topic from the graph-constrained eligible set — until
    time runs out or all candidates are covered.
    """
    graph = load_concept_graph()

    # ── Step 2: Resolve raw topic names → graph concepts ──────────────────
    all_raw = analysis.weak_topics + analysis.mastered_topics
    resolved = resolve_topics(all_raw, use_llm_fallback=True)

    weak_concepts = list(dict.fromkeys(resolved[t] for t in analysis.weak_topics))
    mastered_concepts = list(dict.fromkeys(resolved[t] for t in analysis.mastered_topics))

    # ── Step 3: Graph Expansion (add prerequisites) ───────────────────────
    candidates = expand_weak_topics(weak_concepts, mastered_concepts, graph)

    # ── Steps 5–6: Iterative loop with time budget ───────────────────────
    remaining = list(candidates)
    completed: List[str] = []
    ordered: List[OrderedTopic] = []
    weak_set = set(weak_concepts)

    time_remaining = analysis.time_budget
    time_allocated = 0.0

    while remaining and time_remaining > 0:
        # Step 5: What's eligible right now?
        eligible = get_eligible_topics(remaining, completed, mastered_concepts, graph)

        if not eligible:
            break

        # Gap 2 fix: compute what each eligible topic unlocks
        unlock_map = get_unlock_map(eligible, remaining, completed, mastered_concepts, graph)

        # Step 6: LLM picks the best next topic
        if len(eligible) == 1:
            topic = eligible[0]
            est = _estimate_hours(
                topic, remaining, time_remaining,
                skill_map=analysis.skill_map, weak_set=weak_set,
            )
            pick = {
                "selected": topic,
                "estimated_hours": est,
                "reason": "Only eligible topic",
            }
        else:
            pick = _llm_pick_next(
                eligible=eligible,
                completed=completed,
                weak_concepts=weak_concepts,
                skill_map=analysis.skill_map,
                difficulty_tolerance=analysis.difficulty_tolerance,
                unlock_map=unlock_map,
                time_remaining=time_remaining,
                weak_set=weak_set,
            )

        selected = pick["selected"]
        estimated_hours = pick["estimated_hours"]

        # Gap 1 fix: respect time budget
        if estimated_hours > time_remaining:
            # If this is a target topic and we have at least some time, compress it
            if selected in weak_set and time_remaining >= 0.5:
                estimated_hours = round(time_remaining, 1)
                pick["reason"] += " (compressed to fit remaining time)"
            else:
                # Not enough time — skip this and all remaining
                break

        # Gap 3 fix: mark whether this is a target or prerequisite
        is_target = selected in weak_set

        ordered.append(OrderedTopic(
            topic=selected,
            is_target=is_target,
            estimated_hours=estimated_hours,
            reason=pick["reason"],
        ))

        completed.append(selected)
        remaining.remove(selected)
        time_allocated += estimated_hours
        time_remaining -= estimated_hours

    # Anything still in remaining was skipped due to time
    skipped = remaining

    return OrderingResult(
        ordered_topics=ordered,
        mastered_topics=mastered_concepts,
        candidate_topics=candidates,
        time_budget=analysis.time_budget,
        time_allocated=time_allocated,
        topics_skipped=skipped,
    )

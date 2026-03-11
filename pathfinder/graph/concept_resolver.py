# graph/concept_resolver.py
"""
Concept Resolver — Runtime logic for the prerequisite graph layer.

Responsibilities:
  1. Load the three static JSON files (concept_graph, topic_to_concept, allowed_concepts).
  2. Resolve arbitrary topic strings → valid graph concepts.
  3. Expand weak topics into their prerequisite closure (deterministic).
  4. Compute eligible topics (whose prerequisites are satisfied).

This module is purely structural.  It never calls the Planning Agent
or decides learning order — that is the LLM's job downstream.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Set

from llm.client import chat as llm_chat

# ── Path constants ────────────────────────────────────────────────────────────

_GRAPH_DIR = Path(__file__).resolve().parent

_CONCEPT_GRAPH_PATH = _GRAPH_DIR / "concept_graph.json"
_TOPIC_TO_CONCEPT_PATH = _GRAPH_DIR / "topic_to_concept.json"
_ALLOWED_CONCEPTS_PATH = _GRAPH_DIR / "allowed_concepts.json"

# ── Loaders (cached at module level) ─────────────────────────────────────────


def _load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_concept_graph() -> Dict[str, List[str]]:
    """Return {concept: [prerequisite_concepts, ...]}."""
    return _load_json(_CONCEPT_GRAPH_PATH)


def load_topic_to_concept() -> Dict[str, str]:
    """Return {fine_topic: concept}. Excludes the _comment key."""
    raw = _load_json(_TOPIC_TO_CONCEPT_PATH)
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def load_allowed_concepts() -> List[str]:
    """Return the closed set of valid concept names."""
    return _load_json(_ALLOWED_CONCEPTS_PATH)


# ── Topic → Concept resolution ───────────────────────────────────────────────
def _llm_map_topic(topic: str, allowed: List[str]) -> str:
    """
    Lightweight LLM fallback — called only when static mapping misses.
    Returns a concept from the allowed list, or 'unknown'.
    """
    allowed_str = ", ".join(allowed)
    prompt = (
        "You are a classification assistant.\n\n"
        "Task:\n"
        "Map the given fine-grained DSA topic to exactly ONE high-level concept.\n\n"
        f"Allowed concepts:\n[{allowed_str}]\n\n"
        f'Topic:\n"{topic}"\n\n'
        "Rules:\n"
        "- Choose only from the allowed concepts.\n"
        '- If no concept fits well, return "unknown".\n'
        "- Do not explain.\n"
        "- Return JSON only.\n\n"
        "Output format:\n"
        '{\n  "concept": "<one_allowed_concept_or_unknown>"\n}'
    )

    try:
        text = llm_chat(messages=[{"role": "user", "content": prompt}])

        # Parse the JSON response robustly
        parsed = json.loads(text)
        concept = parsed.get("concept", "unknown")
        return concept if concept in allowed else "unknown"

    except Exception:
        return "unknown"


def map_topic_to_concept(
    topic: str,
    mapping: Dict[str, str],
    allowed_concepts: List[str],
    use_llm_fallback: bool = True,
) -> str:
    """
    Resolve a single topic string to a valid graph concept.

    Resolution order:
      1. Direct match in allowed_concepts  (topic IS a concept)
      2. Static lookup in topic_to_concept  (human-curated)
      3. LLM fallback                       (closed-set classification)
      4. Return topic as-is                  (safe leaf — no prerequisites)
    """
    normalised = topic.strip().lower().replace(" ", "_").replace("-", "_")

    # 1. Already a valid concept?
    if normalised in allowed_concepts:
        return normalised

    # 2. Static mapping?
    if normalised in mapping:
        return mapping[normalised]

    # 3. LLM fallback (optional — can be disabled for tests)
    if use_llm_fallback:
        concept = _llm_map_topic(normalised, allowed_concepts)
        if concept != "unknown":
            return concept

    # 4. Unknown topic → treat as leaf (no prerequisites)
    return normalised


def resolve_topics(
    topics: List[str],
    use_llm_fallback: bool = True,
) -> Dict[str, str]:
    """
    Batch-resolve a list of raw topics.
    Returns {raw_topic: resolved_concept}.
    """
    mapping = load_topic_to_concept()
    allowed = load_allowed_concepts()
    return {
        t: map_topic_to_concept(t, mapping, allowed, use_llm_fallback)
        for t in topics
    }


# ── Graph expansion (prerequisite closure) ────────────────────────────────────


def get_prerequisites(concept: str, graph: Dict[str, List[str]]) -> Set[str]:
    """
    Return the full transitive prerequisite closure for a concept.
    Uses iterative BFS to avoid stack issues on deep chains.
    """
    visited: Set[str] = set()
    queue = list(graph.get(concept, []))

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        queue.extend(graph.get(current, []))

    return visited


def expand_weak_topics(
    weak_concepts: List[str],
    mastered_concepts: List[str],
    graph: Optional[Dict[str, List[str]]] = None,
) -> List[str]:
    """
    Step 3 of the pipeline: Graph Expansion.

    Given weak concepts, gather all their transitive prerequisites,
    remove anything already mastered, and return a deduplicated set
    (as a list, unordered — ordering is the LLM's job later).
    """
    if graph is None:
        graph = load_concept_graph()

    mastered_set = set(mastered_concepts)
    candidate_set: Set[str] = set()

    for concept in weak_concepts:
        candidate_set.add(concept)
        candidate_set.update(get_prerequisites(concept, graph))

    # Remove mastered topics — no need to re-learn them
    candidate_set -= mastered_set

    return list(candidate_set)


# ── Eligible topic computation ────────────────────────────────────────────────
def get_eligible_topics(
    candidate_topics: List[str],
    completed_topics: List[str],
    mastered_topics: List[str],
    graph: Optional[Dict[str, List[str]]] = None,
) -> List[str]:
    """
    Step 5 of the pipeline: Eligible Topic Identification.

    A topic is *eligible* if ALL its prerequisites are either:
      - already completed in the roadmap, OR
      - already mastered by the student.

    Returns the list of currently eligible (unlocked) topics.
    """
    if graph is None:
        graph = load_concept_graph()

    satisfied = set(completed_topics) | set(mastered_topics)
    eligible: List[str] = []

    for topic in candidate_topics:
        prereqs = set(graph.get(topic, []))
        if prereqs.issubset(satisfied):
            eligible.append(topic)

    return eligible


# ── Downstream impact analysis ────────────────────────────────────────────────
def get_unlock_map(
    eligible: List[str],
    remaining: List[str],
    completed: List[str],
    mastered: List[str],
    graph: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, List[str]]:
    """
    For each eligible topic, compute which remaining topics it would
    unlock if completed next. This gives the LLM concrete downstream
    impact data instead of guessing from general DSA knowledge.

    Returns {eligible_topic: [topics_it_would_unlock]}.
    """
    if graph is None:
        graph = load_concept_graph()

    satisfied = set(completed) | set(mastered)
    not_yet_eligible = set(remaining) - set(eligible)
    unlock_map: Dict[str, List[str]] = {}

    for candidate in eligible:
        # Simulate: if we completed this candidate, what new topics become eligible?
        new_satisfied = satisfied | {candidate}
        newly_unlocked = []
        for blocked in not_yet_eligible:
            prereqs = set(graph.get(blocked, []))
            if prereqs.issubset(new_satisfied):
                newly_unlocked.append(blocked)
        unlock_map[candidate] = newly_unlocked

    return unlock_map

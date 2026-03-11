# main.py — Run the full pipeline (Steps 1–6) with step-by-step output

from schemas.models import StudentSnapshot
from agents.skill_analyzer import run_skill_analyzer, analyze_skills
from agents.topic_ordering import run_ordering_loop
from graph.concept_resolver import (
    resolve_topics,
    expand_weak_topics,
    get_eligible_topics,
    get_unlock_map,
    load_concept_graph,
)


def main():
    # ── Student Input ─────────────────────────────────────────────────────
    student = StudentSnapshot(
        trees="weak",
        dp="very weak",
        arrays="strong",
        graphs="medium",
        recursion="medium",
        binary_search="medium",
        sorting="strong",
        time_available_hours=20,
    )

    print("=" * 60)
    print("STUDENT INPUT")
    print("=" * 60)
    for field, value in student.model_dump().items():
        print(f"  {field}: {value}")

    # ── Step 1: Skill Analyzer Agent ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 1: Skill Analyzer Agent")
    print("=" * 60)
    result = run_skill_analyzer(student)
    analysis = result.analysis

    print(f"  Weak topics:     {analysis.weak_topics}")
    print(f"  Mastered topics: {analysis.mastered_topics}")
    print(f"  Priority order:  {analysis.priority_topics}")
    print(f"  Difficulty:      {analysis.difficulty_tolerance}")
    print(f"  Time budget:     {analysis.time_budget}h")
    print(f"\n  LLM Summary:\n  {result.summary}")

    # ── Step 2: Topic Resolution (Weak Topic List) ────────────────────────
    print("\n" + "=" * 60)
    print("STEP 2: Topic Resolution (raw names → graph concepts)")
    print("=" * 60)
    all_raw = analysis.weak_topics + analysis.mastered_topics
    resolved = resolve_topics(all_raw, use_llm_fallback=True)

    for raw, concept in resolved.items():
        tag = " (mapped)" if raw != concept else ""
        print(f"  {raw} → {concept}{tag}")

    weak_concepts = list(dict.fromkeys(resolved[t] for t in analysis.weak_topics))
    mastered_concepts = list(dict.fromkeys(resolved[t] for t in analysis.mastered_topics))

    # ── Step 3: Graph Expansion (Prerequisites) ──────────────────────────
    print("\n" + "=" * 60)
    print("STEP 3: Graph Expansion (add prerequisites)")
    print("=" * 60)
    graph = load_concept_graph()
    candidates = expand_weak_topics(weak_concepts, mastered_concepts, graph)

    print(f"  Weak concepts:    {weak_concepts}")
    print(f"  Mastered:         {mastered_concepts}")
    print(f"  Prerequisites pulled in:")
    prereq_only = [c for c in candidates if c not in weak_concepts]
    if prereq_only:
        for p in prereq_only:
            print(f"    + {p}")
    else:
        print(f"    (none — all prerequisites already mastered)")
    print(f"  Candidate set:    {sorted(candidates)}")

    # ── Step 4: Candidate Topic Set ───────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 4: Candidate Topic Set (structural, unordered)")
    print("=" * 60)
    for c in sorted(candidates):
        role = "TARGET" if c in weak_concepts else "PREREQUISITE"
        prereqs = graph.get(c, [])
        print(f"  {c} [{role}] — prereqs: {prereqs if prereqs else 'none'}")

    # ── Step 5: Initial Eligible Topics ───────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 5: Eligible Topic Identification (initial)")
    print("=" * 60)
    eligible = get_eligible_topics(candidates, [], mastered_concepts, graph)
    print(f"  Mastered (count as satisfied): {mastered_concepts}")
    print(f"  Initially eligible: {eligible}")
    for t in sorted(candidates):
        prereqs = graph.get(t, [])
        satisfied = all(p in mastered_concepts for p in prereqs)
        status = "ELIGIBLE" if t in eligible else "BLOCKED"
        print(f"    {t}: prereqs={prereqs} → {status}")

    # ── Step 6: Iterative Ordering Loop (LLM + Graph) ────────────────────
    print("\n" + "=" * 60)
    print("STEP 6: Iterative Ordering Loop (LLM + Graph)")
    print("=" * 60)
    ordering = run_ordering_loop(analysis)

    for i, topic in enumerate(ordering.ordered_topics, 1):
        tag = "TARGET" if topic.is_target else "PREREQ"
        print(f"\n  Iteration {i}:")
        print(f"    Selected: {topic.topic} ({topic.estimated_hours}h) [{tag}]")
        print(f"    Reason:   {topic.reason}")

    # ── Final Summary ─────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("FINAL ROADMAP")
    print("=" * 60)
    for i, topic in enumerate(ordering.ordered_topics, 1):
        tag = "TARGET" if topic.is_target else "PREREQ"
        print(f"  {i}. {topic.topic:<25} {topic.estimated_hours:>5.1f}h  [{tag}]")

    print(f"\n  Total time:  {ordering.time_allocated:.1f} / {ordering.time_budget:.1f}h")
    if ordering.topics_skipped:
        print(f"  Skipped:     {ordering.topics_skipped}")
    else:
        print(f"  All candidate topics covered.")


if __name__ == "__main__":
    main()

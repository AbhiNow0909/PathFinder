# agents/validation_agent.py
"""
Step 9: Validation and Self-Correction Agent.

Deterministically checks the final generated roadmap (Step 8) for:
1. Prerequisite Sequence Violations (using the symbolic Dependency Graph)
2. Total Time Overflow
3. Structural Consistency
"""

from schemas.models import FinalRoadmap, SkillAnalysis

def validate_roadmap(
    roadmap: FinalRoadmap,
    analysis: SkillAnalysis,
    graph: dict[str, list[str]]
) -> list[str]:
    """
    Validates a generated roadmap against constraints.
    Returns a list of error feedback strings. If empty, the roadmap is valid.
    """
    errors = []

    # 1. Check time boundary
    if roadmap.total_time > analysis.time_budget + 0.1: # Allow slight float drift
        errors.append(
            f"Time violation: Total time ({roadmap.total_time}h) exceeds the "
            f"budget ({analysis.time_budget}h). You MUST stay within the budget."
        )

    seen_topics = set()
    mastered_topics = set(analysis.mastered_topics)

    # 2. Check logical prerequisite sequencing & structural duplicates
    for step in roadmap.roadmap:
        topic = step.topic

        if topic in seen_topics:
            errors.append(
                f"Duplicate topic: '{topic}' appears multiple times. It should only appear once."
            )
            continue

        if step.time_estimate_hours < 0:
            errors.append(f"Invalid time: '{topic}' has a negative time estimate.")

        # Prerequisite check against the graph
        prereqs = graph.get(topic, [])
        missing_prereqs = []
        for p in prereqs:
            # If the student hasn't mastered the prereq natively,
            # and it wasn't placed earlier in the roadmap, it's a violation.
            if p not in mastered_topics and p not in seen_topics:
                # Need to also check if the prerequisite is actually in the roadmap
                # Wait, if it wasn't seen earlier, it's either out of order or entirely missing.
                missing_prereqs.append(p)

        if missing_prereqs:
            errors.append(
                f"Prerequisite violation: Topic '{topic}' requires {missing_prereqs} "
                f"to be mastered or studied BEFORE it. Rearrange the sequence so "
                f"prerequisites appear first."
            )

        seen_topics.add(topic)

    return errors

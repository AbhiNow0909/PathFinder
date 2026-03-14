# agents/planning_agent.py
"""
Step 8 of the pipeline: Reasoning-Aware Planning Agent.

Takes the chosen topics and their retrieved curriculum context,
and prompts the LLM to generate the final, explainable roadmap.
The LLM generates explicit reasoning for each step, grounding
recommendations in the curriculum references and the student's profile.
"""

from __future__ import annotations

import json
import re

from llm.client import chat as llm_chat
from schemas.models import (
    SkillAnalysis,
    CurriculumEntry,
    FinalRoadmap,
    RoadmapStep,
)

PLANNER_SYSTEM_PROMPT = """You are an expert DSA AI tutor generating a final, personalized study roadmap.

You will receive:
1. The student's current skill profile and constraints.
2. A sequence of topics they must study (already logically ordered to respect prerequisites).
3. Retrieved curriculum context and references for each topic.

Your task is to generate the final roadmap.
For each topic in the sequence, you must output a structured step containing:
- The topic name
- The estimated hours allocated
- A specific reason WHY they are studying it now, connecting their weak/strong status to the curriculum context provided.
- The exact curriculum reference provided to you.

Constraints:
- Do NOT change the sequencing. Maintain the exact order provided.
- Do NOT change the estimated hours provided.
- Make the 'reason' short (1-2 sentences), encouraging, and directly related to the provided curriculum context. Let them know if it's a primary target or just a prerequisite.
- Do NOT hallucinate references. Keep exactly the reference provided.

Output MUST be valid JSON matching this schema:
{
  "roadmap": [
    {
      "step": 1,
      "topic": "<topic>",
      "time_estimate_hours": <hours>,
      "reason": "<explanation>",
      "reference": "<exact reference provided>"
    }
  ],
  "total_time": <sum of all hours>
}
Return ONLY the JSON. No markdown blocking, no other text."""


def generate_roadmap(
    entries: list[CurriculumEntry],
    analysis: SkillAnalysis,
    feedback: str | None = None,
) -> FinalRoadmap:
    """
    Generate the final roadmap using LLM reasoning grounded in the curriculum.
    Optional `feedback` is injected if the validation loop rejected the previous attempt.
    """
    if not entries:
        return FinalRoadmap(roadmap=[], total_time=0.0)

    # Build the context payload for the LLM
    context_blocks = []
    total_budgeted_time = 0.0
    for i, entry in enumerate(entries, 1):
        role = "Target Focus" if entry.is_target else "Prerequisite Review"
        total_budgeted_time += entry.estimated_hours
        
        block = (
            f"Step {i}: {entry.concept}\n"
            f"  Role: {role}\n"
            f"  Allocated Time: {entry.estimated_hours}h\n"
            f"  Reference: {entry.reference}\n"
            f"  Curriculum Context:\n"
            f"    {entry.context[:800]}...\n"  # truncate to prevent token bloat
        )
        context_blocks.append(block)

    curriculum_payload = "\n\n".join(context_blocks)

    user_prompt = (
        f"STUDENT PROFILE:\n"
        f"- Weak concepts: {analysis.weak_topics}\n"
        f"- Mastered concepts: {analysis.mastered_topics}\n"
        f"- Total time budget: {analysis.time_budget}h\n"
        f"- Time allocated: {total_budgeted_time:.1f}h\n\n"
        f"SEQUENCE & CURRICULUM CONTEXT:\n"
        f"{curriculum_payload}\n\n"
        f"Generate the final JSON roadmap."
    )

    if feedback:
        user_prompt += (
            f"\n\n🚨 PREVIOUS ATTEMPT FAILED VALIDATION 🚨\n"
            f"The previous roadmap you generated violated constraints:\n"
            f"{feedback}\n\n"
            f"You MUST fix these structural problems in your new generated JSON."
        )

    try:
        response_text = llm_chat(
            messages=[
                {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2, # slightly more deterministic for structural JSON
        )

        # Robust JSON extraction
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in LLM response")
            
        parsed = json.loads(json_match.group())
        return FinalRoadmap(**parsed)

    except Exception as e:
        print(f"  [Warning] LLM planning failed or returned invalid JSON: {e}")
        print("  [Warning] Falling back to deterministic assembly.")
        
        # Deterministic fallback assembling the objects directly
        steps = []
        for i, entry in enumerate(entries, 1):
            role_desc = "critical weak area" if entry.is_target else "necessary prerequisite"
            steps.append(RoadmapStep(
                step=i,
                topic=entry.concept,
                time_estimate_hours=entry.estimated_hours,
                reason=f"Recommended as a {role_desc} based on the {entry.concept} curriculum.",
                reference=entry.reference
            ))
            
        return FinalRoadmap(roadmap=steps, total_time=total_budgeted_time)

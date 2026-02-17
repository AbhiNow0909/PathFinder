# schemas/models.py

from pydantic import BaseModel, Field
from typing import Dict, List, Literal

# ── Literals ──────────────────────────────────────────────────────────────────

SkillLevel = Literal["very weak", "weak", "medium", "strong", "very strong"]
DifficultyTolerance = Literal["easy", "medium", "hard"]

# ── Input Model ───────────────────────────────────────────────────────────────

class StudentSnapshot(BaseModel):
    trees: SkillLevel = "medium"
    dp: SkillLevel = "medium"
    arrays: SkillLevel = "medium"
    graphs: SkillLevel = "medium"
    recursion: SkillLevel = "medium"
    binary_search: SkillLevel = "medium"
    sorting: SkillLevel = "medium"
    time_available_hours: float = Field(..., gt=0, le=100)

# ── Intermediate Output (Layer 1) ─────────────────────────────────────────────

class SkillAnalysis(BaseModel):
    priority_topics: List[str]
    mastered_topics: List[str]
    weak_topics: List[str]
    time_budget: float
    difficulty_tolerance: DifficultyTolerance
    skill_map: Dict[str, SkillLevel]

# ── Final Output (Layer 1 + Layer 2 combined) ─────────────────────────────────

class SkillAnalyzerOutput(BaseModel):
    analysis: SkillAnalysis
    summary: str = Field(..., description="LLM-generated natural language summary")
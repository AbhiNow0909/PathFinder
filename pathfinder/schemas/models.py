from pydantic import BaseModel, Field
from typing import Dict, List, Literal

SkillLevel = Literal["very weak", "weak", "medium", "strong", "very strong"]
DifficultyTolerance = Literal["easy", "medium", "hard"]

class StudentSnapshot(BaseModel):
    trees: SkillLevel = "medium"
    dp: SkillLevel = "medium"
    arrays: SkillLevel = "medium"
    graphs: SkillLevel = "medium"
    recursion: SkillLevel = "medium"
    binary_search: SkillLevel = "medium"
    sorting: SkillLevel = "medium"
    time_available_hours: float = Field(..., gt=0, le=100)

class SkillAnalysis(BaseModel):
    priority_topics: List[str]       # ordered by urgency
    mastered_topics: List[str]
    weak_topics: List[str]           # all weak/very weak
    time_budget: float
    difficulty_tolerance: DifficultyTolerance
    skill_map: Dict[str, SkillLevel] # original scores preserved
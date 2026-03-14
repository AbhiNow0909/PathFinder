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
    time_available_hours: float = Field(..., gt=0, le=500)

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

# ── Step 6: Iterative Ordering Output ─────────────────────────────────────────

class OrderedTopic(BaseModel):
    topic: str
    is_target: bool = Field(..., description="True if this is a weak topic the student needs; False if prerequisite filler")
    estimated_hours: float = Field(..., description="LLM-estimated time for this topic")
    reason: str = Field(..., description="LLM's reason for picking this topic at this position")

class OrderingResult(BaseModel):
    ordered_topics: List[OrderedTopic]
    mastered_topics: List[str]
    candidate_topics: List[str]
    time_budget: float = Field(..., description="Total time the student has")
    time_allocated: float = Field(..., description="Total time allocated across ordered topics")
    topics_skipped: List[str] = Field(default_factory=list, description="Candidates dropped due to time budget")

# ── Step 7: RAG Curriculum Output ─────────────────────────────────────────────

class CurriculumEntry(BaseModel):
    concept: str
    is_target: bool
    estimated_hours: float
    context: str = Field(..., description="The concatenated text chunks retrieved from ChromaDB")
    reference: str = Field(..., description="The source material reference, e.g., 'CLRS (chapter.md)'")
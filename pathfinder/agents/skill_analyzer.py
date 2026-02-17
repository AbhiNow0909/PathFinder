# agents/skill_analyzer.py

from schemas.models import StudentSnapshot, SkillAnalysis, DifficultyTolerance
import ollama

WEAK_THRESHOLDS = {"very weak", "weak"}
STRONG_THRESHOLDS = {"strong", "very strong"}

SKILL_PRIORITY_ORDER = {
    "very weak": 0,
    "weak": 1,
    "medium": 2,
    "strong": 3,
    "very strong": 4
}

# ── Layer 1: Deterministic Rules ──────────────────────────────────────────────

def infer_difficulty_tolerance(skill_map: dict) -> DifficultyTolerance:
    avg = sum(SKILL_PRIORITY_ORDER[v] for v in skill_map.values()) / len(skill_map)
    if avg < 1.5:
        return "easy"
    elif avg < 2.8:
        return "medium"
    else:
        return "hard"

def analyze_skills(snapshot: StudentSnapshot) -> SkillAnalysis:
    skill_map = snapshot.model_dump(exclude={"time_available_hours"})
    
    weak_topics = [t for t, lvl in skill_map.items() if lvl in WEAK_THRESHOLDS]
    mastered_topics = [t for t, lvl in skill_map.items() if lvl in STRONG_THRESHOLDS]
    priority_topics = sorted(weak_topics, key=lambda t: SKILL_PRIORITY_ORDER[skill_map[t]])
    
    return SkillAnalysis(
        priority_topics=priority_topics,
        mastered_topics=mastered_topics,
        weak_topics=weak_topics,
        time_budget=snapshot.time_available_hours,
        difficulty_tolerance=infer_difficulty_tolerance(skill_map),
        skill_map=skill_map
    )

# ── Layer 2: LLM Enrichment ───────────────────────────────────────────────────

def get_llm_summary(analysis: SkillAnalysis) -> str:
    
    system_prompt = """You are an expert DSA (Data Structures & Algorithms) learning coach.
Your job is to analyze a student's skill profile and provide a clear, honest, and actionable summary.

Guidelines:
- Be direct and specific — name the actual topics
- Prioritize the weakest areas without overwhelming the student
- Acknowledge strengths briefly, focus on gaps
- Keep time constraints in mind when giving advice
- Write in plain prose, no bullet points or headers
- Respond in 2-3 sentences only"""

    user_prompt = f"""Here is the student's current DSA skill profile:

Weak topics (need focus): {analysis.weak_topics}
Mastered topics (can skip): {analysis.mastered_topics}
Available study time: {analysis.time_budget} hours
Difficulty tolerance: {analysis.difficulty_tolerance}
Full skill breakdown: {analysis.skill_map}

Summarize their learning situation and what they should focus on given their time budget."""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response["message"]["content"]

# ── Public Interface ──────────────────────────────────────────────────────────

def run_skill_analyzer(snapshot: StudentSnapshot) -> dict:
    analysis = analyze_skills(snapshot)        # fast, always runs
    summary = get_llm_summary(analysis)        # LLM enrichment on top
    return {
        "analysis": analysis,
        "summary": summary
    }
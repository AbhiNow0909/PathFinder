# tests/test_skill_analyzer.py

from unittest import result
import pytest
from unittest.mock import patch, MagicMock
from agents.skill_analyzer import analyze_skills, get_llm_summary, run_skill_analyzer
from schemas.models import StudentSnapshot, SkillAnalyzerOutput

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def weak_student():
    return StudentSnapshot(
        dp="very weak",
        trees="weak",
        arrays="strong",
        graphs="medium",
        recursion="weak",
        binary_search="medium",
        sorting="strong",
        time_available_hours=5
    )

@pytest.fixture
def strong_student():
    return StudentSnapshot(
        dp="strong",
        trees="very strong",
        arrays="strong",
        graphs="strong",
        recursion="very strong",
        binary_search="strong",
        sorting="strong",
        time_available_hours=3
    )

@pytest.fixture
def mixed_student():
    return StudentSnapshot(
        dp="very weak",
        trees="medium",
        arrays="medium",
        graphs="weak",
        recursion="medium",
        binary_search="medium",
        sorting="medium",
        time_available_hours=8
    )

# ── Layer 1: analyze_skills() Tests ──────────────────────────────────────────

class TestAnalyzeSkills:

    def test_weak_topics_identified(self, weak_student):
        result = analyze_skills(weak_student)
        assert "dp" in result.weak_topics
        assert "trees" in result.weak_topics
        assert "recursion" in result.weak_topics

    def test_mastered_topics_identified(self, weak_student):
        result = analyze_skills(weak_student)
        assert "arrays" in result.mastered_topics
        assert "sorting" in result.mastered_topics

    def test_priority_order_very_weak_first(self, weak_student):
        result = analyze_skills(weak_student)
        # dp is "very weak", should come before "weak" topics
        assert result.priority_topics[0] == "dp"

    def test_time_budget_preserved(self, weak_student):
        result = analyze_skills(weak_student)
        assert result.time_budget == 5.0

    def test_difficulty_tolerance_easy_for_weak_student(self, weak_student):
        result = analyze_skills(weak_student)
        assert result.difficulty_tolerance == "easy"

    def test_difficulty_tolerance_hard_for_strong_student(self, strong_student):
        result = analyze_skills(strong_student)
        assert result.difficulty_tolerance == "hard"

    def test_no_weak_topics_for_strong_student(self, strong_student):
        result = analyze_skills(strong_student)
        assert result.weak_topics == []
        assert result.priority_topics == []

    def test_skill_map_excludes_time(self, weak_student):
        result = analyze_skills(weak_student)
        assert "time_available_hours" not in result.skill_map

    def test_medium_topics_not_in_weak_or_mastered(self, mixed_student):
        result = analyze_skills(mixed_student)
        assert "trees" not in result.weak_topics
        assert "trees" not in result.mastered_topics


# ── Layer 2: get_llm_summary() Tests ─────────────────────────────────────────

class TestGetLlmSummary:

    @patch("agents.skill_analyzer.ollama.chat")
    def test_returns_string(self, mock_chat, weak_student):
        mock_chat.return_value = {
            "message": {"content": "Student should focus on DP and Trees."}
        }
        analysis = analyze_skills(weak_student)
        result = get_llm_summary(analysis)
        assert isinstance(result, str)
        assert len(result) > 0

    @patch("agents.skill_analyzer.ollama.chat")
    def test_ollama_called_once(self, mock_chat, weak_student):
        mock_chat.return_value = {
            "message": {"content": "Some summary."}
        }
        analysis = analyze_skills(weak_student)
        get_llm_summary(analysis)
        mock_chat.assert_called_once()

    @patch("agents.skill_analyzer.ollama.chat")
    def test_correct_model_used(self, mock_chat, weak_student):
        mock_chat.return_value = {
            "message": {"content": "Some summary."}
        }
        analysis = analyze_skills(weak_student)
        get_llm_summary(analysis)
        call_args = mock_chat.call_args
        assert call_args.kwargs["model"] == "llama3"

    @patch("agents.skill_analyzer.ollama.chat")
    def test_system_and_user_prompts_sent(self, mock_chat, weak_student):
        mock_chat.return_value = {
            "message": {"content": "Some summary."}
        }
        analysis = analyze_skills(weak_student)
        get_llm_summary(analysis)
        messages = mock_chat.call_args.kwargs["messages"]
        roles = [m["role"] for m in messages]
        assert "system" in roles
        assert "user" in roles

    @patch("agents.skill_analyzer.ollama.chat")
    def test_llm_failure_raises(self, mock_chat, weak_student):
        mock_chat.side_effect = Exception("Ollama connection failed")
        analysis = analyze_skills(weak_student)
        with pytest.raises(Exception, match="Ollama connection failed"):
            get_llm_summary(analysis)


# ── Integration: run_skill_analyzer() Tests ───────────────────────────────────

class TestRunSkillAnalyzer:

    @patch("agents.skill_analyzer.ollama.chat")
    def test_returns_analysis_and_summary(self, mock_chat, weak_student):
        mock_chat.return_value = {"message": {"content": "Focus on DP and Trees first."}}
        result = run_skill_analyzer(weak_student)
        assert isinstance(result, SkillAnalyzerOutput)

    @patch("agents.skill_analyzer.ollama.chat")
    def test_analysis_is_skill_analysis_type(self, mock_chat, weak_student):
        from schemas.models import SkillAnalysis
        mock_chat.return_value = {
            "message": {"content": "Some summary."}
        }
        result = run_skill_analyzer(weak_student)
        assert isinstance(result["analysis"], SkillAnalysis)

    @patch("agents.skill_analyzer.ollama.chat")
    def test_summary_is_string(self, mock_chat, weak_student):
        mock_chat.return_value = {
            "message": {"content": "Some summary."}
        }
        result = run_skill_analyzer(weak_student)
        assert isinstance(result["summary"], str)
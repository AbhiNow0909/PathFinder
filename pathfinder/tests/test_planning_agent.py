# tests/test_planning_agent.py

import json
import pytest
from unittest.mock import patch
from schemas.models import SkillAnalysis, CurriculumEntry, FinalRoadmap
from agents.planning_agent import generate_roadmap

@pytest.fixture
def mock_analysis():
    return SkillAnalysis(
        priority_topics=["trees"],
        mastered_topics=["arrays"],
        weak_topics=["trees"],
        time_budget=5.0,
        difficulty_tolerance="medium",
        skill_map={"trees": "weak"}
    )

@pytest.fixture
def mock_entries():
    return [
        CurriculumEntry(
            concept="recursion",
            is_target=False,
            estimated_hours=1.0,
            context="Recursion is when a function calls itself.",
            reference="CLRS Chapter 4"
        ),
        CurriculumEntry(
            concept="trees",
            is_target=True,
            estimated_hours=2.0,
            context="A tree is an acyclic connected graph.",
            reference="CLRS Chapter 12"
        )
    ]

class TestPlanningAgent:

    @patch("agents.planning_agent.llm_chat")
    def test_generate_roadmap_success(self, mock_chat, mock_entries, mock_analysis):
        # Mock valid JSON response
        mock_response = {
            "roadmap": [
                {
                    "step": 1,
                    "topic": "recursion",
                    "time_estimate_hours": 1.0,
                    "reason": "Prerequisite review based on CLRS.",
                    "reference": "CLRS Chapter 4"
                },
                {
                    "step": 2,
                    "topic": "trees",
                    "time_estimate_hours": 2.0,
                    "reason": "Target topic for weak area.",
                    "reference": "CLRS Chapter 12"
                }
            ],
            "total_time": 3.0
        }
        mock_chat.return_value = json.dumps(mock_response)
        
        result = generate_roadmap(mock_entries, mock_analysis)
        
        assert isinstance(result, FinalRoadmap)
        assert len(result.roadmap) == 2
        assert result.total_time == 3.0
        assert result.roadmap[0].topic == "recursion"
        assert "Prerequisite" in result.roadmap[0].reason

    @patch("agents.planning_agent.llm_chat")
    def test_generate_roadmap_fallback_invalid_json(self, mock_chat, mock_entries, mock_analysis):
        # Mock bad response
        mock_chat.return_value = "This is not JSON at all."
        
        result = generate_roadmap(mock_entries, mock_analysis)
        
        # Should drop to deterministic fallback
        assert isinstance(result, FinalRoadmap)
        assert len(result.roadmap) == 2
        assert result.total_time == 3.0
        assert "necessary prerequisite" in result.roadmap[0].reason
        assert "critical weak area" in result.roadmap[1].reason

    def test_empty_entries_returns_empty_roadmap(self, mock_analysis):
        result = generate_roadmap([], mock_analysis)
        assert len(result.roadmap) == 0
        assert result.total_time == 0.0

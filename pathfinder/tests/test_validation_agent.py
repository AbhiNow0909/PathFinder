# tests/test_validation_agent.py

import pytest
from schemas.models import FinalRoadmap, RoadmapStep, SkillAnalysis
from agents.validation_agent import validate_roadmap

@pytest.fixture
def mock_analysis():
    return SkillAnalysis(
        priority_topics=["trees", "dp"],
        mastered_topics=["arrays"],
        weak_topics=["trees", "dp"],
        time_budget=10.0,
        difficulty_tolerance="medium",
        skill_map={"trees": "weak", "dp": "very weak"}
    )

@pytest.fixture
def mock_graph():
    return {
        "arrays": [],
        "recursion": [],
        "trees": ["recursion"],
        "dp": ["recursion", "arrays"]
    }

def test_validate_roadmap_success(mock_analysis, mock_graph):
    roadmap = FinalRoadmap(
        roadmap=[
            RoadmapStep(step=1, topic="recursion", time_estimate_hours=2.0, reason="prereq", reference="ref"),
            RoadmapStep(step=2, topic="trees", time_estimate_hours=3.0, reason="target", reference="ref"),
            RoadmapStep(step=3, topic="dp", time_estimate_hours=5.0, reason="target", reference="ref")
        ],
        total_time=10.0
    )
    
    errors = validate_roadmap(roadmap, mock_analysis, mock_graph)
    assert not errors, "Expected no errors for a valid roadmap"

def test_validate_time_overflow(mock_analysis, mock_graph):
    roadmap = FinalRoadmap(
        roadmap=[
            RoadmapStep(step=1, topic="recursion", time_estimate_hours=5.0, reason="prereq", reference="ref"),
            RoadmapStep(step=2, topic="trees", time_estimate_hours=6.0, reason="target", reference="ref")
        ],
        total_time=11.0 # Exceeds budget of 10.0
    )
    
    errors = validate_roadmap(roadmap, mock_analysis, mock_graph)
    assert len(errors) == 1
    assert "Time violation" in errors[0]

def test_validate_prerequisite_violation(mock_analysis, mock_graph):
    roadmap = FinalRoadmap(
        roadmap=[
            # 'trees' scheduled before its prerequisite 'recursion'
            RoadmapStep(step=1, topic="trees", time_estimate_hours=5.0, reason="target", reference="ref"),
            RoadmapStep(step=2, topic="recursion", time_estimate_hours=5.0, reason="prereq", reference="ref")
        ],
        total_time=10.0
    )
    
    errors = validate_roadmap(roadmap, mock_analysis, mock_graph)
    assert len(errors) == 1
    assert "Prerequisite violation" in errors[0]
    assert "requires ['recursion']" in errors[0]

def test_validate_prerequisite_satisfied_by_mastery(mock_analysis, mock_graph):
    # 'dp' requires 'arrays' and 'recursion'. 'arrays' is natively mastered.
    roadmap = FinalRoadmap(
        roadmap=[
            RoadmapStep(step=1, topic="recursion", time_estimate_hours=5.0, reason="prereq", reference="ref"),
            RoadmapStep(step=2, topic="dp", time_estimate_hours=5.0, reason="target", reference="ref")
        ],
        total_time=10.0
    )
    
    errors = validate_roadmap(roadmap, mock_analysis, mock_graph)
    assert not errors, "Native mastery 'arrays' should satisfy the prerequisite check"

def test_validate_duplicate_topics(mock_analysis, mock_graph):
    roadmap = FinalRoadmap(
        roadmap=[
            RoadmapStep(step=1, topic="recursion", time_estimate_hours=5.0, reason="prereq", reference="ref"),
            RoadmapStep(step=2, topic="recursion", time_estimate_hours=5.0, reason="duplicate", reference="ref")
        ],
        total_time=10.0
    )
    
    errors = validate_roadmap(roadmap, mock_analysis, mock_graph)
    assert len(errors) == 1
    assert "Duplicate topic" in errors[0]

# PathFinder
A constraint-aware, curriculum-grounded, neuro-symbolic Generative AI system that produces logically valid, explainable, and adaptive DSA learning roadmaps using LLM reasoning, RAG, and dependency graph enforcement.

# Adaptive Learning Roadmap Generator  
## A Neuro-Symbolic, Constraint-Aware Generative AI System for Curriculum Planning

---

# 1. Introduction

The **Adaptive Learning Roadmap Generator** is a Generative AI system designed to produce a short, personalized Data Structures & Algorithms (DSA) study roadmap based on a student's current coding profile snapshot.

Unlike generic study planners, this system:

- Adapts to the student's strengths and weaknesses
- Respects prerequisite relationships between topics
- Operates under strict time constraints
- Grounds all recommendations in curriculum content
- Uses structured reasoning and validation

The system combines:

- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- A Topic Dependency Graph (symbolic reasoning)
- A Reasoning-Aware Planning Agent
- A Validation and Self-Correction loop

This results in a **hybrid neuro-symbolic planning framework** for explainable adaptive learning.

---

# 2. Problem Statement

Students preparing for DSA interviews often face the following challenges:

- They follow generic topic lists.
- They ignore prerequisite dependencies.
- They over-practice strong areas.
- They lack structured, time-aware guidance.
- They receive non-explainable recommendations.

Existing AI-based systems:
- Do not enforce logical prerequisite constraints.
- Do not explicitly reason under time limits.
- Do not validate structural correctness of study plans.
- Often hallucinate topic sequencing.

This project addresses these limitations by building a **constraint-aware, curriculum-grounded adaptive roadmap generator**.

---

# 3. System Inputs

## 3.1 Student Skill Snapshot

The system takes a structured snapshot of a student’s current abilities.

Example:

```json
{
  "trees": "weak",
  "dp": "very weak",
  "arrays": "strong",
  "graphs": "medium",
  "time_available_hours": 5
}
```

## 3.2 Curriculum Corpus (For RAG)

The system stores curriculum materials in a vector database, including:

-Course syllabi
-CLRS textbook chapters
-Lecture slides
-Topic explanations
-Difficulty metadata
-Estimated learning time
-Reference links

All roadmap decisions are grounded in this retrieved curriculum content.

# 4. System Architecture
```json
Student Snapshot
      ↓
(1) Skill Analyzer Agent
      ↓
(2) Weak Topic List
      ↓
(3) Graph Expansion (Prerequisites)
      ↓
(4) Candidate Topic Set
      ↓
(5) Eligible Topic Identification (Graph)
      ↓
(6) Iterative Ordering Loop (LLM + Graph)
      ↓
(7) RAG Retrieval (Grounding)
      ↓
(8) Planning Agent (LLM Reasoning)
      ↓
(9) Validation Agent
      ↓
Final Roadmap
```
# 5. Core Components

## 5.1 Skill Analyzer Agent
**Purpose**

Transforms raw student statistics into structured planning signals.

**Responsibilities**

-Identify weak topics
-Identify mastered topics
-Rank priority areas
-Extract time constraints
-Determine difficulty tolerance

Example output:

```json
{
  "priority_topics": ["dp", "trees"],
  "mastered_topics": ["arrays"],
  "time_budget": 5,
  "difficulty_tolerance": "medium"
}
```

## 5.2 Topic Dependency Graph (Symbolic Layer)
Purpose

Encodes prerequisite relationships between DSA topics as a Directed Acyclic Graph (DAG).

Example Representation

```json
{
  "Recursion": [],
  "Arrays": [],
  "Trees": ["Recursion"],
  "Binary Search Tree": ["Trees"],
  "Dynamic Programming": ["Recursion", "Arrays"],
  "Graphs": [],
  "BFS": ["Graphs"],
  "DFS": ["Graphs", "Recursion"]
}
```

Role in System

-Expands weak topics to include required prerequisites
-Enforces valid topic ordering
-Enables topological sorting
-Enables deterministic validation

This prevents logically invalid study sequences.

## 5.3 Curriculum Retrieval (RAG)

The Retrieval-Augmented Generation module:

-Retrieves prerequisite descriptions
-Retrieves topic explanations
-Retrieves estimated learning time
-Retrieves textbook or syllabus references

This ensures:

-Curriculum alignment
-Reduced hallucination
-Explainable recommendations
-Source-grounded reasoning

## 5.4 Reasoning-Aware Planning Agent

This is the core generative component.

Instead of a single prompt, the agent reasons under constraints.

Constraints Enforced

-Total time ≤ available time
-Weak topics must be prioritized
-No topic before its prerequisites
-Strong topics should not dominate
-Each step must include explanation and reference

Responsibilities

-Select appropriate subgraph of topics
-Allocate time per topic
-Generate structured roadmap steps
-Provide reasoning for sequencing
-Justify decisions using curriculum references

This transforms the system into a constraint-aware AI planner.

## 5.5 Validation & Self-Correction Agent

After roadmap generation, the system validates:

-Prerequisite ordering violations
-Time overflow
-Weak-topic coverage
-Structural consistency

If violations occur:

-The planner is re-invoked with feedback
-The roadmap is revised
-The process repeats until valid

This introduces a self-correcting agentic loop, improving reliability.

# 6. Output Format

Example:

```json
{
  "roadmap": [
    {
      "step": 1,
      "topic": "Recursion",
      "time_estimate_hours": 1.5,
      "reason": "Prerequisite for Trees and Dynamic Programming",
      "reference": "CLRS Chapter 15"
    },
    {
      "step": 2,
      "topic": "Binary Trees",
      "time_estimate_hours": 1.5,
      "reason": "Weak topic dependent on Recursion",
      "reference": "Lecture 7 Notes"
    }
  ],
  "total_time": 5
}
```

Each step includes:

-Topic
-Time estimate
-Reason for inclusion
-Curriculum reference

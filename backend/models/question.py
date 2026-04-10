"""
Pydantic models for Questions in the SQL Practice Platform.

These models define the shape of question data served by the API.
"""

from __future__ import annotations
from enum import Enum
from pydantic import BaseModel


class Difficulty(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class QuestionSummary(BaseModel):
    """Lightweight model for question list views."""
    id: int
    title: str
    difficulty: Difficulty
    tags: list[str]
    tables_used: list[str]


class Question(BaseModel):
    """Full question model with all details."""
    id: int
    title: str
    difficulty: Difficulty
    tags: list[str]
    problem_statement: str
    tables_used: list[str]
    hint: str
    explanation: str
    solution_sql: str
    pyspark_equivalent: str
    expected_output_columns: list[str]
    expected_row_count: int
    requires_order: bool = False


class QuestionListResponse(BaseModel):
    """Response model for paginated question list."""
    questions: list[QuestionSummary]
    total: int
    tags: list[str]


class QuestionDetailResponse(BaseModel):
    """Response model for single question detail — hides solution by default."""
    question: Question
    # These are excluded from default view but available via reveal endpoints
    solution_visible: bool = False

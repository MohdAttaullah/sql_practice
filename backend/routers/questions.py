"""
Questions router — serves the question bank from questions.json.

Supports filtering by difficulty, tags, search, and pagination.
"""

from __future__ import annotations
import json
from pathlib import Path
from fastapi import APIRouter, Query, HTTPException
from backend.models.question import (
    Question,
    QuestionSummary,
    QuestionListResponse,
    Difficulty,
)

router = APIRouter(prefix="/api/questions", tags=["questions"])

# Load question bank from JSON file at module level
_QUESTIONS_PATH = Path(__file__).parent.parent / "data" / "questions.json"
_questions: list[dict] = []
_all_tags: list[str] = []


def _load_questions():
    global _questions, _all_tags
    if not _questions:
        with open(_QUESTIONS_PATH, "r", encoding="utf-8") as f:
            _questions = json.load(f)
        # Collect unique tags
        tags_set = set()
        for q in _questions:
            for tag in q.get("tags", []):
                tags_set.add(tag)
        _all_tags = sorted(tags_set)


@router.get("", response_model=QuestionListResponse)
def list_questions(
    difficulty: str | None = Query(None, description="Filter by difficulty: Easy, Medium, Hard"),
    tag: str | None = Query(None, description="Filter by tag"),
    search: str | None = Query(None, description="Search in title and problem statement"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    """Return paginated, filterable list of questions."""
    _load_questions()
    filtered = _questions

    if difficulty:
        filtered = [q for q in filtered if q["difficulty"].lower() == difficulty.lower()]
    if tag:
        filtered = [q for q in filtered if tag.lower() in [t.lower() for t in q.get("tags", [])]]
    if search:
        search_lower = search.lower()
        filtered = [
            q for q in filtered
            if search_lower in q["title"].lower() or search_lower in q.get("problem_statement", "").lower()
        ]

    total = len(filtered)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = filtered[start:end]

    summaries = [
        QuestionSummary(
            id=q["id"],
            title=q["title"],
            difficulty=q["difficulty"],
            tags=q.get("tags", []),
            tables_used=q.get("tables_used", []),
        )
        for q in page_items
    ]

    return QuestionListResponse(questions=summaries, total=total, tags=_all_tags)


@router.get("/tags", response_model=list[str])
def get_all_tags():
    """Return all unique tags used across questions."""
    _load_questions()
    return _all_tags


@router.get("/{question_id}", response_model=Question)
def get_question(question_id: int):
    """Return full question details by ID."""
    _load_questions()
    for q in _questions:
        if q["id"] == question_id:
            return Question(**q)
    raise HTTPException(status_code=404, detail=f"Question {question_id} not found")


@router.get("/{question_id}/solution")
def get_solution(question_id: int):
    """Return the solution SQL and PySpark equivalent."""
    _load_questions()
    for q in _questions:
        if q["id"] == question_id:
            return {
                "question_id": question_id,
                "solution_sql": q["solution_sql"],
                "pyspark_equivalent": q.get("pyspark_equivalent", ""),
                "explanation": q.get("explanation", ""),
            }
    raise HTTPException(status_code=404, detail=f"Question {question_id} not found")

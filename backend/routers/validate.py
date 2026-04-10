"""
Validate router — compares user query output against expected answer.

Runs both the user SQL and the solution SQL, then uses the evaluator
to produce a verdict and diagnostic feedback.
"""

import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database.engine import execute_query
from backend.services.evaluator import evaluate
from backend.models.progress import record_attempt

router = APIRouter(prefix="/api", tags=["validate"])

# Load questions for solution lookup
_QUESTIONS_PATH = Path(__file__).parent.parent / "data" / "questions.json"
_questions_cache: list[dict] | None = None


def _get_questions() -> list[dict]:
    global _questions_cache
    if _questions_cache is None:
        with open(_QUESTIONS_PATH, "r", encoding="utf-8") as f:
            _questions_cache = json.load(f)
    return _questions_cache


class ValidateRequest(BaseModel):
    question_id: int
    user_sql: str


class ValidateResponse(BaseModel):
    verdict: str  # correct, partial, incorrect
    feedback: list[str]
    user_columns: list[str]
    user_rows: list[list]
    user_row_count: int
    expected_columns: list[str]
    expected_rows: list[list]
    expected_row_count: int


@router.post("/validate", response_model=ValidateResponse)
def validate_answer(request: ValidateRequest):
    """
    Validate user SQL answer against the expected solution.

    1. Runs the user's SQL
    2. Runs the solution SQL
    3. Compares outputs using the evaluator
    4. Records the attempt in progress tracking
    5. Returns verdict + feedback + both result sets
    """
    # Find the question
    questions = _get_questions()
    question = None
    for q in questions:
        if q["id"] == request.question_id:
            question = q
            break
    if question is None:
        raise HTTPException(status_code=404, detail=f"Question {request.question_id} not found")

    # Execute user SQL
    user_sql = request.user_sql.strip()
    if not user_sql:
        raise HTTPException(status_code=400, detail="SQL query cannot be empty")

    try:
        user_columns, user_rows = execute_query(user_sql)
    except RuntimeError as e:
        # Record failed attempt
        record_attempt(request.question_id, user_sql, "incorrect", f"SQL Error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"SQL Error: {str(e)}")

    # Execute solution SQL
    try:
        expected_columns, expected_rows = execute_query(question["solution_sql"])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running solution SQL (this is a bug): {str(e)}"
        )

    # Evaluate
    requires_order = question.get("requires_order", False)
    result = evaluate(
        user_columns=user_columns,
        user_rows=user_rows,
        expected_columns=expected_columns,
        expected_rows=expected_rows,
        requires_order=requires_order,
    )

    # Record attempt
    record_attempt(
        question_id=request.question_id,
        user_sql=user_sql,
        verdict=result.verdict.value,
        feedback="; ".join(result.feedback),
    )

    return ValidateResponse(
        verdict=result.verdict.value,
        feedback=result.feedback,
        user_columns=user_columns,
        user_rows=user_rows[:200],  # Cap for response size
        user_row_count=len(user_rows),
        expected_columns=expected_columns,
        expected_rows=expected_rows[:200],
        expected_row_count=len(expected_rows),
    )

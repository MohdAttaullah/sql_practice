"""
Progress router — track user attempts, bookmarks, and notes.

Provides endpoints for the Progress Tracker page and workspace features.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from backend.models.progress import (
    get_all_progress,
    get_progress_for_question,
    update_bookmark,
    update_notes,
    get_recent_attempts,
)

router = APIRouter(prefix="/api/progress", tags=["progress"])


class BookmarkRequest(BaseModel):
    question_id: int
    bookmarked: bool


class NotesRequest(BaseModel):
    question_id: int
    notes: str


@router.get("")
def get_progress_summary():
    """
    Return aggregate progress stats for the dashboard.
    """
    all_progress = get_all_progress()
    total_attempted = len(all_progress)
    total_solved = sum(1 for p in all_progress if p["is_solved"])
    total_bookmarked = sum(1 for p in all_progress if p["is_bookmarked"])

    # Per-verdict breakdown
    verdict_counts = {"correct": 0, "partial": 0, "incorrect": 0}
    for p in all_progress:
        v = p.get("best_verdict", "unattempted")
        if v in verdict_counts:
            verdict_counts[v] += 1

    return {
        "total_attempted": total_attempted,
        "total_solved": total_solved,
        "total_bookmarked": total_bookmarked,
        "verdict_breakdown": verdict_counts,
        "questions": all_progress,
    }


@router.get("/recent")
def get_recent():
    """Return recent attempts for the dashboard activity feed."""
    return get_recent_attempts(limit=20)


@router.get("/{question_id}")
def get_question_progress(question_id: int):
    """Return progress for a single question."""
    return get_progress_for_question(question_id)


@router.post("/bookmark")
def toggle_bookmark(request: BookmarkRequest):
    """Toggle bookmark on a question."""
    update_bookmark(request.question_id, request.bookmarked)
    return {"status": "ok", "question_id": request.question_id, "bookmarked": request.bookmarked}


@router.post("/notes")
def save_notes(request: NotesRequest):
    """Save user notes for a question."""
    update_notes(request.question_id, request.notes)
    return {"status": "ok", "question_id": request.question_id}

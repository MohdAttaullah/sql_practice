"""
SQLAlchemy ORM models for progress tracking.

Uses SQLite to persist user progress locally.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from pathlib import Path
import os


class Base(DeclarativeBase):
    pass


class QuestionAttempt(Base):
    """Records each attempt a user makes on a question."""
    __tablename__ = "question_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, nullable=False, index=True)
    user_sql = Column(Text, nullable=False)
    verdict = Column(String(20), nullable=False)  # correct, partial, incorrect
    feedback = Column(Text, nullable=True)
    attempted_at = Column(DateTime, default=datetime.utcnow)


class QuestionProgress(Base):
    """Aggregate progress for each question."""
    __tablename__ = "question_progress"

    question_id = Column(Integer, primary_key=True)
    total_attempts = Column(Integer, default=0)
    best_verdict = Column(String(20), default="unattempted")  # correct, partial, incorrect, unattempted
    is_solved = Column(Boolean, default=False)
    is_bookmarked = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    last_attempted_at = Column(DateTime, nullable=True)


# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

_PROGRESS_DB = os.getenv(
    "PROGRESS_DB_PATH",
    str(Path(__file__).parent.parent / "data" / "progress.db"),
)
_engine = None
_SessionLocal = None


def _get_engine():
    global _engine
    if _engine is None:
        Path(_PROGRESS_DB).parent.mkdir(parents=True, exist_ok=True)
        _engine = create_engine(f"sqlite:///{_PROGRESS_DB}", echo=False)
        Base.metadata.create_all(_engine)
    return _engine


def get_session() -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=_get_engine())
    return _SessionLocal()


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def record_attempt(question_id: int, user_sql: str, verdict: str, feedback: str | None = None):
    """Record a new attempt and update aggregate progress."""
    session = get_session()
    try:
        # Record the attempt
        attempt = QuestionAttempt(
            question_id=question_id,
            user_sql=user_sql,
            verdict=verdict,
            feedback=feedback,
        )
        session.add(attempt)

        # Update aggregate progress
        progress = session.query(QuestionProgress).filter_by(question_id=question_id).first()
        if progress is None:
            progress = QuestionProgress(question_id=question_id)
            session.add(progress)

        progress.total_attempts = (progress.total_attempts or 0) + 1
        progress.last_attempted_at = datetime.utcnow()

        # Update best verdict (correct > partial > incorrect)
        verdict_rank = {"correct": 3, "partial": 2, "incorrect": 1, "unattempted": 0}
        current_rank = verdict_rank.get(progress.best_verdict, 0)
        new_rank = verdict_rank.get(verdict, 0)
        if new_rank > current_rank:
            progress.best_verdict = verdict
        if verdict == "correct":
            progress.is_solved = True

        session.commit()
    finally:
        session.close()


def get_progress_for_question(question_id: int) -> dict:
    """Return progress summary for a single question."""
    session = get_session()
    try:
        progress = session.query(QuestionProgress).filter_by(question_id=question_id).first()
        if progress is None:
            return {
                "question_id": question_id,
                "total_attempts": 0,
                "best_verdict": "unattempted",
                "is_solved": False,
                "is_bookmarked": False,
                "notes": None,
                "last_attempted_at": None,
            }
        return {
            "question_id": progress.question_id,
            "total_attempts": progress.total_attempts,
            "best_verdict": progress.best_verdict,
            "is_solved": progress.is_solved,
            "is_bookmarked": progress.is_bookmarked,
            "notes": progress.notes,
            "last_attempted_at": progress.last_attempted_at.isoformat() if progress.last_attempted_at else None,
        }
    finally:
        session.close()


def get_all_progress() -> list[dict]:
    """Return progress for all attempted questions."""
    session = get_session()
    try:
        rows = session.query(QuestionProgress).all()
        return [
            {
                "question_id": r.question_id,
                "total_attempts": r.total_attempts,
                "best_verdict": r.best_verdict,
                "is_solved": r.is_solved,
                "is_bookmarked": r.is_bookmarked,
                "notes": r.notes,
                "last_attempted_at": r.last_attempted_at.isoformat() if r.last_attempted_at else None,
            }
            for r in rows
        ]
    finally:
        session.close()


def update_bookmark(question_id: int, bookmarked: bool):
    """Toggle bookmark status for a question."""
    session = get_session()
    try:
        progress = session.query(QuestionProgress).filter_by(question_id=question_id).first()
        if progress is None:
            progress = QuestionProgress(question_id=question_id, is_bookmarked=bookmarked)
            session.add(progress)
        else:
            progress.is_bookmarked = bookmarked
        session.commit()
    finally:
        session.close()


def update_notes(question_id: int, notes: str):
    """Save user notes for a question."""
    session = get_session()
    try:
        progress = session.query(QuestionProgress).filter_by(question_id=question_id).first()
        if progress is None:
            progress = QuestionProgress(question_id=question_id, notes=notes)
            session.add(progress)
        else:
            progress.notes = notes
        session.commit()
    finally:
        session.close()


def get_recent_attempts(limit: int = 20) -> list[dict]:
    """Return the most recent attempts across all questions."""
    session = get_session()
    try:
        rows = (
            session.query(QuestionAttempt)
            .order_by(QuestionAttempt.attempted_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": r.id,
                "question_id": r.question_id,
                "verdict": r.verdict,
                "attempted_at": r.attempted_at.isoformat() if r.attempted_at else None,
            }
            for r in rows
        ]
    finally:
        session.close()

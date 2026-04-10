"""
Evaluation engine for comparing user SQL output against expected output.

Provides smart comparison that handles:
- Row order normalization (unless explicitly required)
- Column order normalization
- Null-aware comparison
- Diagnostic feedback on mismatches
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class Verdict(str, Enum):
    CORRECT = "correct"
    PARTIAL = "partial"
    INCORRECT = "incorrect"


@dataclass
class EvaluationResult:
    verdict: Verdict
    feedback: list[str]
    user_row_count: int
    expected_row_count: int
    user_columns: list[str]
    expected_columns: list[str]

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict.value,
            "feedback": self.feedback,
            "user_row_count": self.user_row_count,
            "expected_row_count": self.expected_row_count,
            "user_columns": self.user_columns,
            "expected_columns": self.expected_columns,
        }


def evaluate(
    user_columns: list[str],
    user_rows: list[list],
    expected_columns: list[str],
    expected_rows: list[list],
    requires_order: bool = False,
) -> EvaluationResult:
    """
    Compare user query output against expected output.

    Args:
        user_columns: Column names from user query.
        user_rows: Row data from user query.
        expected_columns: Column names from expected query.
        expected_rows: Row data from expected query.
        requires_order: If True, row order matters.

    Returns:
        EvaluationResult with verdict and feedback.
    """
    feedback: list[str] = []

    # ── Step 1: Column check ──────────────────────────────────────────────
    user_cols_lower = [c.lower() for c in user_columns]
    expected_cols_lower = [c.lower() for c in expected_columns]

    if set(user_cols_lower) != set(expected_cols_lower):
        missing = set(expected_cols_lower) - set(user_cols_lower)
        extra = set(user_cols_lower) - set(expected_cols_lower)
        if missing:
            feedback.append(f"Missing columns: {', '.join(sorted(missing))}")
        if extra:
            feedback.append(f"Extra columns: {', '.join(sorted(extra))}")

        # Check if it's just aliases
        if len(user_cols_lower) == len(expected_cols_lower):
            feedback.append("Column count matches but names differ — check your column aliases.")
            # Try comparing values ignoring column names
            value_match = _compare_rows(user_rows, expected_rows, requires_order)
            if value_match:
                return EvaluationResult(
                    verdict=Verdict.PARTIAL,
                    feedback=["Values are correct but column names don't match expected output."],
                    user_row_count=len(user_rows),
                    expected_row_count=len(expected_rows),
                    user_columns=user_columns,
                    expected_columns=expected_columns,
                )
        return EvaluationResult(
            verdict=Verdict.INCORRECT,
            feedback=feedback,
            user_row_count=len(user_rows),
            expected_row_count=len(expected_rows),
            user_columns=user_columns,
            expected_columns=expected_columns,
        )

    # ── Step 2: Reorder user columns to match expected order ──────────────
    if user_cols_lower != expected_cols_lower:
        col_index_map = {col: idx for idx, col in enumerate(user_cols_lower)}
        reorder = [col_index_map[col] for col in expected_cols_lower]
        user_rows = [[row[i] for i in reorder] for row in user_rows]
        user_columns = [user_columns[i] for i in reorder]

    # ── Step 3: Row count check ───────────────────────────────────────────
    if len(user_rows) != len(expected_rows):
        if len(user_rows) > len(expected_rows):
            feedback.append(
                f"Too many rows: got {len(user_rows)}, expected {len(expected_rows)}. "
                "Possible duplicate rows introduced — check your JOIN or missing DISTINCT."
            )
        else:
            feedback.append(
                f"Too few rows: got {len(user_rows)}, expected {len(expected_rows)}. "
                "Check your JOIN condition or WHERE filter."
            )
        return EvaluationResult(
            verdict=Verdict.INCORRECT,
            feedback=feedback,
            user_row_count=len(user_rows),
            expected_row_count=len(expected_rows),
            user_columns=user_columns,
            expected_columns=expected_columns,
        )

    # ── Step 4: Value comparison ──────────────────────────────────────────
    if _compare_rows(user_rows, expected_rows, requires_order):
        return EvaluationResult(
            verdict=Verdict.CORRECT,
            feedback=["✅ Perfect! Your query produces the correct result."],
            user_row_count=len(user_rows),
            expected_row_count=len(expected_rows),
            user_columns=user_columns,
            expected_columns=expected_columns,
        )

    # ── Step 5: Diagnose specific issues ──────────────────────────────────
    feedback.extend(_diagnose(user_rows, expected_rows, expected_columns))

    # Check if it's a partial match (most rows correct)
    matching_rows = _count_matching_rows(user_rows, expected_rows)
    match_pct = matching_rows / len(expected_rows) if expected_rows else 0

    verdict = Verdict.PARTIAL if match_pct >= 0.5 else Verdict.INCORRECT
    return EvaluationResult(
        verdict=verdict,
        feedback=feedback,
        user_row_count=len(user_rows),
        expected_row_count=len(expected_rows),
        user_columns=user_columns,
        expected_columns=expected_columns,
    )


def _normalize_value(val) -> str:
    """Normalize a value for comparison — handles None, float precision, etc."""
    if val is None:
        return "__NULL__"
    if isinstance(val, float):
        return f"{val:.4f}"
    return str(val).strip()


def _row_to_tuple(row: list) -> tuple:
    """Convert a row to a normalized tuple for comparison."""
    return tuple(_normalize_value(v) for v in row)


def _compare_rows(user_rows: list[list], expected_rows: list[list], requires_order: bool) -> bool:
    """Compare two sets of rows, optionally ignoring order."""
    if requires_order:
        return all(
            _row_to_tuple(u) == _row_to_tuple(e)
            for u, e in zip(user_rows, expected_rows)
        )
    else:
        user_set = sorted([_row_to_tuple(r) for r in user_rows])
        expected_set = sorted([_row_to_tuple(r) for r in expected_rows])
        return user_set == expected_set


def _count_matching_rows(user_rows: list[list], expected_rows: list[list]) -> int:
    """Count how many user rows match expected rows (unordered)."""
    expected_set = [_row_to_tuple(r) for r in expected_rows]
    count = 0
    for row in user_rows:
        t = _row_to_tuple(row)
        if t in expected_set:
            count += 1
            expected_set.remove(t)
    return count


def _diagnose(user_rows: list[list], expected_rows: list[list], columns: list[str]) -> list[str]:
    """Generate specific feedback about what's wrong."""
    feedback = []

    # Check for NULL-related issues
    for col_idx, col_name in enumerate(columns):
        user_nulls = sum(1 for r in user_rows if r[col_idx] is None)
        expected_nulls = sum(1 for r in expected_rows if r[col_idx] is None)
        if user_nulls != expected_nulls:
            feedback.append(
                f"NULL handling issue in column '{col_name}': "
                f"your result has {user_nulls} NULLs, expected {expected_nulls}."
            )

    # Check for numeric aggregation issues
    for col_idx, col_name in enumerate(columns):
        try:
            user_vals = [float(r[col_idx]) for r in user_rows if r[col_idx] is not None]
            expected_vals = [float(r[col_idx]) for r in expected_rows if r[col_idx] is not None]
            if user_vals and expected_vals:
                user_sum = sum(user_vals)
                expected_sum = sum(expected_vals)
                if abs(user_sum - expected_sum) > 0.01:
                    feedback.append(
                        f"Aggregation may be off in column '{col_name}': "
                        f"sum is {user_sum:.2f}, expected {expected_sum:.2f}."
                    )
        except (ValueError, TypeError):
            continue

    if not feedback:
        feedback.append("Values differ from expected output — check your logic carefully.")

    return feedback

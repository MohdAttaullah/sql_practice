"""Tests for the evaluation engine."""
import pytest
from backend.services.evaluator import evaluate, Verdict


def test_exact_match():
    result = evaluate(
        user_columns=["id", "name"], user_rows=[[1, "Alice"], [2, "Bob"]],
        expected_columns=["id", "name"], expected_rows=[[1, "Alice"], [2, "Bob"]],
    )
    assert result.verdict == Verdict.CORRECT


def test_unordered_match():
    result = evaluate(
        user_columns=["id", "name"], user_rows=[[2, "Bob"], [1, "Alice"]],
        expected_columns=["id", "name"], expected_rows=[[1, "Alice"], [2, "Bob"]],
        requires_order=False,
    )
    assert result.verdict == Verdict.CORRECT


def test_order_mismatch_when_required():
    result = evaluate(
        user_columns=["id", "name"], user_rows=[[2, "Bob"], [1, "Alice"]],
        expected_columns=["id", "name"], expected_rows=[[1, "Alice"], [2, "Bob"]],
        requires_order=True,
    )
    assert result.verdict != Verdict.CORRECT


def test_column_reorder():
    result = evaluate(
        user_columns=["name", "id"], user_rows=[["Alice", 1], ["Bob", 2]],
        expected_columns=["id", "name"], expected_rows=[[1, "Alice"], [2, "Bob"]],
    )
    assert result.verdict == Verdict.CORRECT


def test_extra_rows():
    result = evaluate(
        user_columns=["id"], user_rows=[[1], [2], [3]],
        expected_columns=["id"], expected_rows=[[1], [2]],
    )
    assert result.verdict == Verdict.INCORRECT
    assert any("Too many rows" in f for f in result.feedback)


def test_missing_rows():
    result = evaluate(
        user_columns=["id"], user_rows=[[1]],
        expected_columns=["id"], expected_rows=[[1], [2]],
    )
    assert result.verdict == Verdict.INCORRECT
    assert any("Too few rows" in f for f in result.feedback)


def test_wrong_columns():
    result = evaluate(
        user_columns=["id", "val"], user_rows=[[1, 10]],
        expected_columns=["id", "name"], expected_rows=[[1, "Alice"]],
    )
    assert result.verdict == Verdict.INCORRECT
    assert any("Missing columns" in f for f in result.feedback)


def test_null_handling():
    result = evaluate(
        user_columns=["id", "val"], user_rows=[[1, None], [2, 10]],
        expected_columns=["id", "val"], expected_rows=[[1, 5], [2, 10]],
    )
    assert result.verdict != Verdict.CORRECT


def test_float_precision():
    result = evaluate(
        user_columns=["val"], user_rows=[[1.00001]],
        expected_columns=["val"], expected_rows=[[1.00002]],
    )
    assert result.verdict == Verdict.CORRECT  # within 4 decimal rounding


def test_partial_match():
    result = evaluate(
        user_columns=["id", "val"], user_rows=[[1, 10], [2, 99]],
        expected_columns=["id", "val"], expected_rows=[[1, 10], [2, 20]],
    )
    assert result.verdict == Verdict.PARTIAL

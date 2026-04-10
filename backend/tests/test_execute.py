"""Integration tests for the execute and validate endpoints."""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_execute_simple():
    r = client.post("/api/execute", json={"sql": "SELECT 1 AS val"})
    assert r.status_code == 200
    data = r.json()
    assert data["columns"] == ["val"]
    assert data["rows"] == [[1]]


def test_execute_select_from_table():
    r = client.post("/api/execute", json={"sql": "SELECT COUNT(*) AS cnt FROM customers"})
    assert r.status_code == 200
    assert r.json()["rows"][0][0] == 20


def test_execute_write_blocked():
    r = client.post("/api/execute", json={"sql": "DROP TABLE customers"})
    assert r.status_code == 400


def test_execute_syntax_error():
    r = client.post("/api/execute", json={"sql": "SELEC bad"})
    assert r.status_code == 400


def test_list_questions():
    r = client.get("/api/questions")
    assert r.status_code == 200
    assert r.json()["total"] >= 50


def test_filter_questions_by_difficulty():
    r = client.get("/api/questions?difficulty=Easy")
    assert r.status_code == 200
    for q in r.json()["questions"]:
        assert q["difficulty"] == "Easy"


def test_get_question_detail():
    r = client.get("/api/questions/1")
    assert r.status_code == 200
    assert r.json()["id"] == 1


def test_list_datasets():
    r = client.get("/api/datasets")
    assert r.status_code == 200
    names = [d["name"] for d in r.json()]
    assert "customers" in names
    assert "orders" in names


def test_dataset_preview():
    r = client.get("/api/datasets/customers")
    assert r.status_code == 200
    assert r.json()["row_count"] == 20


def test_validate_correct():
    # Question 6: duplicate orders — simple GROUP BY HAVING
    r = client.post("/api/validate", json={
        "question_id": 6,
        "user_sql": "SELECT order_id, COUNT(*) AS occurrence_count FROM orders GROUP BY order_id HAVING COUNT(*)>1"
    })
    assert r.status_code == 200
    assert r.json()["verdict"] == "correct"


def test_validate_wrong():
    r = client.post("/api/validate", json={
        "question_id": 6,
        "user_sql": "SELECT order_id, COUNT(*) AS occurrence_count FROM orders GROUP BY order_id"
    })
    assert r.status_code == 200
    assert r.json()["verdict"] != "correct"

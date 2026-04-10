"""
Execute router — runs user SQL queries against DuckDB and returns results.

Provides a safe, read-only query execution endpoint with error handling.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database.engine import execute_query

router = APIRouter(prefix="/api", tags=["execute"])


class ExecuteRequest(BaseModel):
    sql: str
    limit: int = 1000  # Max rows to return


class ExecuteResponse(BaseModel):
    columns: list[str]
    rows: list[list]
    row_count: int
    truncated: bool


@router.post("/execute", response_model=ExecuteResponse)
def execute_sql(request: ExecuteRequest):
    """
    Execute a user-provided SQL query against the practice database.

    Returns columns and rows. Limited to read-only operations.
    Caps results at `limit` rows (default 1000).
    """
    sql = request.sql.strip()
    if not sql:
        raise HTTPException(status_code=400, detail="SQL query cannot be empty")

    try:
        columns, rows = execute_query(sql)
        truncated = len(rows) > request.limit
        return ExecuteResponse(
            columns=columns,
            rows=rows[:request.limit],
            row_count=len(rows),
            truncated=truncated,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

"""
Datasets router — browse practice tables, schemas, and preview data.

Provides endpoints for the Dataset Explorer page.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from backend.database.engine import (
    get_table_names,
    get_table_schema,
    get_table_preview,
    get_table_row_count,
)

router = APIRouter(prefix="/api/datasets", tags=["datasets"])


class TableInfo(BaseModel):
    name: str
    row_count: int
    column_count: int


class TableSchema(BaseModel):
    column_name: str
    data_type: str
    is_nullable: str


class TableDetailResponse(BaseModel):
    name: str
    row_count: int
    schema_info: list[TableSchema]
    preview_columns: list[str]
    preview_rows: list[list]


@router.get("", response_model=list[TableInfo])
def list_datasets():
    """Return list of all practice tables with basic info."""
    try:
        tables = get_table_names()
        result = []
        for t in tables:
            schema = get_table_schema(t)
            row_count = get_table_row_count(t)
            result.append(TableInfo(name=t, row_count=row_count, column_count=len(schema)))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{table_name}", response_model=TableDetailResponse)
def get_dataset_detail(table_name: str, limit: int = Query(20, ge=1, le=100)):
    """Return schema and preview data for a specific table."""
    try:
        schema = get_table_schema(table_name)
        if not schema:
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

        row_count = get_table_row_count(table_name)
        columns, rows = get_table_preview(table_name, limit)

        return TableDetailResponse(
            name=table_name,
            row_count=row_count,
            schema_info=[TableSchema(**s) for s in schema],
            preview_columns=columns,
            preview_rows=rows,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

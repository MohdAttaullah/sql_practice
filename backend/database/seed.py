"""
Database seeding module.

Creates all tables and populates them with sample data from seed_data.py.
Called automatically on first connection if database doesn't exist.
"""

import duckdb
from backend.data.seed_data import ALL_DATASETS


def seed_all(conn: duckdb.DuckDBPyConnection):
    """
    Create and populate all practice tables.

    Uses DuckDB's native type inference from Python values.
    """
    print("🌱 Seeding practice database...")

    for dataset_fn in ALL_DATASETS:
        table_name, columns, rows = dataset_fn()
        _create_and_insert(conn, table_name, columns, rows)
        print(f"   ✅ {table_name}: {len(rows)} rows")

    print("🎉 Seeding complete!")


def _create_and_insert(
    conn: duckdb.DuckDBPyConnection,
    table_name: str,
    columns: list[str],
    rows: list[tuple],
):
    """Create a table from column names and row tuples using DuckDB's VALUES syntax."""
    # Build CREATE TABLE from first row type inference
    col_types = _infer_types(columns, rows[0])
    col_defs = ", ".join(f'"{col}" {dtype}' for col, dtype in col_types.items())
    conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    conn.execute(f'CREATE TABLE "{table_name}" ({col_defs})')

    # Insert rows using parameterized queries
    placeholders = ", ".join(["?"] * len(columns))
    insert_sql = f'INSERT INTO "{table_name}" VALUES ({placeholders})'
    for row in rows:
        conn.execute(insert_sql, list(row))


def _infer_types(columns: list[str], sample_row: tuple) -> dict[str, str]:
    """Infer DuckDB column types from a Python sample row."""
    type_map = {}
    for col, val in zip(columns, sample_row):
        if val is None:
            type_map[col] = "VARCHAR"
        elif isinstance(val, bool):
            type_map[col] = "BOOLEAN"
        elif isinstance(val, int):
            type_map[col] = "INTEGER"
        elif isinstance(val, float):
            type_map[col] = "DOUBLE"
        elif isinstance(val, str):
            # Check if it looks like a date or timestamp
            if len(val) == 10 and val[4] == "-" and val[7] == "-":
                type_map[col] = "DATE"
            elif len(val) == 19 and ":" in val:
                type_map[col] = "TIMESTAMP"
            else:
                type_map[col] = "VARCHAR"
        else:
            type_map[col] = "VARCHAR"
    return type_map

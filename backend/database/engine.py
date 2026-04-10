"""
DuckDB connection manager for the SQL Practice Platform.

Manages a single DuckDB instance that holds all practice datasets.
The database is seeded on first startup and persisted to disk.
"""

import os
import duckdb
from pathlib import Path

# Database file path — persisted in the backend/data directory
_DB_PATH = os.getenv("DUCKDB_PATH", str(Path(__file__).parent.parent / "data" / "practice.duckdb"))
_connection: duckdb.DuckDBPyConnection | None = None


def get_connection() -> duckdb.DuckDBPyConnection:
    """
    Return the singleton DuckDB connection. Creates and seeds
    the database on first call if it doesn't exist yet.
    """
    global _connection
    if _connection is None:
        db_exists = Path(_DB_PATH).exists()
        Path(_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
        _connection = duckdb.connect(_DB_PATH)
        if not db_exists:
            from backend.database.seed import seed_all
            seed_all(_connection)
    return _connection


def execute_query(sql: str) -> tuple[list[str], list[list]]:
    """
    Execute a read-only SQL query and return (columns, rows).

    Raises RuntimeError on invalid SQL or write operations.
    """
    conn = get_connection()
    # Safety: reject obvious write statements
    stripped = sql.strip().upper()
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE", "COPY"]
    first_word = stripped.split()[0] if stripped else ""
    if first_word in forbidden:
        raise RuntimeError(f"Write operations are not allowed: {first_word}")

    try:
        result = conn.execute(sql)
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        # Convert to plain Python types for JSON serialization
        serialized_rows = []
        for row in rows:
            serialized_row = []
            for val in row:
                if val is None:
                    serialized_row.append(None)
                elif isinstance(val, (int, float, str, bool)):
                    serialized_row.append(val)
                else:
                    serialized_row.append(str(val))
            serialized_rows.append(serialized_row)
        return columns, serialized_rows
    except Exception as e:
        raise RuntimeError(str(e))


def get_table_names() -> list[str]:
    """Return list of all user tables in the database."""
    conn = get_connection()
    result = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' ORDER BY table_name")
    return [row[0] for row in result.fetchall()]


def get_table_schema(table_name: str) -> list[dict]:
    """Return column schema for a given table."""
    conn = get_connection()
    result = conn.execute(
        "SELECT column_name, data_type, is_nullable "
        "FROM information_schema.columns "
        "WHERE table_schema = 'main' AND table_name = ? "
        "ORDER BY ordinal_position",
        [table_name],
    )
    return [
        {"column_name": row[0], "data_type": row[1], "is_nullable": row[2]}
        for row in result.fetchall()
    ]


def get_table_preview(table_name: str, limit: int = 20) -> tuple[list[str], list[list]]:
    """Return (columns, rows) preview for a table — safe, uses identifier quoting."""
    # Validate table name exists to prevent injection
    tables = get_table_names()
    if table_name not in tables:
        raise RuntimeError(f"Table '{table_name}' does not exist")
    return execute_query(f'SELECT * FROM "{table_name}" LIMIT {limit}')


def get_table_row_count(table_name: str) -> int:
    """Return the row count for a table."""
    tables = get_table_names()
    if table_name not in tables:
        raise RuntimeError(f"Table '{table_name}' does not exist")
    conn = get_connection()
    result = conn.execute(f'SELECT COUNT(*) FROM "{table_name}"')
    return result.fetchone()[0]


def close_connection():
    """Close the DuckDB connection (used at shutdown)."""
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None

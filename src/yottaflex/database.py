from __future__ import annotations

import duckdb

from .config import DB_PATH, RAW_DIR, TABLES


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(DB_PATH))


def load_csv_tables(con: duckdb.DuckDBPyConnection) -> dict[str, int]:
    """Load source CSVs into DuckDB staging tables, replacing prior staging data."""
    counts = {}
    for table in TABLES:
        csv_path = (RAW_DIR / f"{table}.csv").as_posix().replace("'", "''")
        con.execute(f"CREATE OR REPLACE TABLE stg_{table} AS SELECT * FROM read_csv_auto('{csv_path}', header=true)")
        counts[table] = con.execute(f"SELECT COUNT(*) FROM stg_{table}").fetchone()[0]
    return counts

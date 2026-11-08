from pathlib import Path
import re
import time

import pandas as pd
from pandas.testing import assert_frame_equal

from src.yottaflex.database import connect


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BASELINE_SQL = (
    PROJECT_ROOT / "sql" / "baseline" / "baseline_queries.sql"
)

OPTIMIZED_SQL = (
    PROJECT_ROOT / "sql" / "optimized" / "optimized_queries.sql"
)

REPORT_DIR = PROJECT_ROOT / "reports"


# ============================================================
# SQL LOADING AND CLEANING
# ============================================================

def load_queries(file_path: Path) -> list[str]:
    """Load SQL statements and remove accidental standalone dots."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    content = file_path.read_text(encoding="utf-8")

    queries = []

    for raw_query in content.split(";"):

        lines = [
            line
            for line in raw_query.splitlines()
            if line.strip() != "."
        ]

        query = "\n".join(lines).strip()

        # Ignore SQL comments when checking for actual statements.
        executable_lines = [
            line
            for line in lines
            if not line.lstrip().startswith("--")
        ]

        executable_sql = "\n".join(executable_lines)

        if re.search(
            r"\b(SELECT|WITH)\b",
            executable_sql,
            re.IGNORECASE
        ):
            queries.append(query)

    if not queries:
        raise ValueError(
            f"No executable SQL queries found in {file_path}"
        )

    return queries


# ============================================================
# QUERY EXECUTION
# ============================================================

def execute_query(con, query: str) -> pd.DataFrame:
    """Execute SQL and return results as a DataFrame."""

    try:
        return con.execute(query).fetchdf()

    except Exception as error:
        print("\nSQL EXECUTION FAILED")
        print("-" * 65)
        print(query)
        print("-" * 65)

        raise RuntimeError(
            f"DuckDB query execution failed: {error}"
        ) from error


# ============================================================
# QUERY PERFORMANCE
# ============================================================

def benchmark_query(
    con,
    query: str,
    repetitions: int = 7
) -> float:
    """Measure median query execution time in milliseconds."""

    # Warm-up execution
    execute_query(con, query)

    execution_times = []

    for _ in range(repetitions):

        start_time = time.perf_counter()

        execute_query(con, query)

        end_time = time.perf_counter()

        execution_times.append(
            (end_time - start_time) * 1000
        )

    return round(
        sorted(execution_times)[len(execution_times) // 2],
        3
    )


# ============================================================
# RESULT VALIDATION
# ============================================================

def results_match(
    baseline_result: pd.DataFrame,
    optimized_result: pd.DataFrame
) -> bool:
    """Compare baseline and optimized query outputs."""

    if list(baseline_result.columns) != list(
        optimized_result.columns
    ):
        return False

    if len(baseline_result) != len(optimized_result):
        return False

    try:

        baseline_sorted = baseline_result.sort_values(
            by=list(baseline_result.columns)
        ).reset_index(drop=True)

        optimized_sorted = optimized_result.sort_values(
            by=list(optimized_result.columns)
        ).reset_index(drop=True)

        assert_frame_equal(
            baseline_sorted,
            optimized_sorted,
            check_dtype=False,
            check_exact=False,
            rtol=1e-9,
            atol=1e-8
        )

        return True

    except (AssertionError, TypeError, ValueError):
        return False


# ============================================================
# EXECUTION PLAN CAPTURE
# ============================================================

def capture_execution_plan(con, query: str) -> str:
    """Capture DuckDB EXPLAIN ANALYZE output."""

    result = con.execute(
        "EXPLAIN ANALYZE " + query
    ).fetchall()

    return "\n".join(
        str(row) for row in result
    )


# ============================================================
# MAIN BENCHMARK FUNCTION
# ============================================================

def run_benchmarks(repetitions: int = 7):

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\n" + "=" * 65)
    print("       YOTTAFLEX AI - SQL PERFORMANCE BENCHMARK")
    print("=" * 65)

    baseline_queries = load_queries(BASELINE_SQL)
    optimized_queries = load_queries(OPTIMIZED_SQL)

    print(f"\nBaseline queries: {len(baseline_queries)}")
    print(f"Optimized queries: {len(optimized_queries)}")

    if len(baseline_queries) != len(optimized_queries):
        raise ValueError(
            "Baseline and optimized query counts do not match."
        )

    results = []
    plans = []

    con = connect()

    try:

        for index, (baseline_sql, optimized_sql) in enumerate(
            zip(baseline_queries, optimized_queries),
            start=1
        ):

            print("\n" + "=" * 65)
            print(f"RUNNING QUERY {index}")
            print("=" * 65)

            # --------------------------------------------
            # Execute baseline and optimized queries
            # --------------------------------------------

            baseline_output = execute_query(
                con,
                baseline_sql
            )

            optimized_output = execute_query(
                con,
                optimized_sql
            )

            # --------------------------------------------
            # Validate result accuracy
            # --------------------------------------------

            is_correct = results_match(
                baseline_output,
                optimized_output
            )

            print(
                f"Baseline rows: {len(baseline_output)}"
            )

            print(
                f"Optimized rows: {len(optimized_output)}"
            )

            print(
                f"Results match: {is_correct}"
            )

            if not is_correct:
                raise AssertionError(
                    f"Query {index}: Baseline and optimized "
                    "results do not match."
                )

            # --------------------------------------------
            # Benchmark execution time
            # --------------------------------------------

            baseline_time = benchmark_query(
                con,
                baseline_sql,
                repetitions
            )

            optimized_time = benchmark_query(
                con,
                optimized_sql,
                repetitions
            )

            # Positive = faster optimized query.
            # Negative = slower optimized query.

            improvement = (
                (baseline_time - optimized_time)
                / baseline_time * 100
                if baseline_time > 0
                else 0
            )

            improvement = round(improvement, 2)

            # --------------------------------------------
            # Store benchmark results
            # --------------------------------------------

            results.append({

                "query_id": index,

                "baseline_ms": baseline_time,

                "optimized_ms": optimized_time,

                "improvement_percent": improvement,

                "results_match": is_correct,

                "baseline_rows": len(baseline_output),

                "optimized_rows": len(optimized_output)

            })

            # --------------------------------------------
            # Capture execution plans
            # --------------------------------------------

            baseline_plan = capture_execution_plan(
                con,
                baseline_sql
            )

            optimized_plan = capture_execution_plan(
                con,
                optimized_sql
            )

            plans.append(
                f"\n{'=' * 65}\n"
                f"QUERY {index} - BASELINE\n"
                f"{'=' * 65}\n"
                f"{baseline_plan}\n"
            )

            plans.append(
                f"\n{'=' * 65}\n"
                f"QUERY {index} - OPTIMIZED\n"
                f"{'=' * 65}\n"
                f"{optimized_plan}\n"
            )

            # --------------------------------------------
            # Print query summary
            # --------------------------------------------

            print(f"\nBaseline time: {baseline_time:.3f} ms")

            print(f"Optimized time: {optimized_time:.3f} ms")

            print(f"Performance improvement: {improvement:.2f}%")

            if improvement > 0:
                print("Status: OPTIMIZED QUERY IS FASTER")

            elif improvement < 0:
                print("Status: OPTIMIZED QUERY IS SLOWER")

            else:
                print("Status: PERFORMANCE IS EQUAL")

        # ====================================================
        # SAVE REPORTS
        # ====================================================

        results_df = pd.DataFrame(results)

        results_df.to_csv(
            REPORT_DIR / "benchmark_results.csv",
            index=False
        )

        (REPORT_DIR / "query_plans.txt").write_text(
            "\n".join(plans),
            encoding="utf-8"
        )

        # ====================================================
        # FINAL SUMMARY
        # ====================================================

        print("\n\n" + "=" * 65)
        print("             FINAL BENCHMARK SUMMARY")
        print("=" * 65)

        print(
            results_df.to_string(index=False)
        )

        average_improvement = results_df[
            "improvement_percent"
        ].mean()

        passed_queries = int(
            results_df["results_match"].sum()
        )

        total_queries = len(results_df)

        print("\n" + "-" * 65)

        print(
            f"Total queries: {total_queries}"
        )

        print(
            f"Correct queries: {passed_queries}"
        )

        print(
            f"Average performance improvement: "
            f"{average_improvement:.2f}%"
        )

        print(
            f"Faster optimized queries: "
            f"{int((results_df['improvement_percent'] > 0).sum())}"
        )

        print(
            f"Slower optimized queries: "
            f"{int((results_df['improvement_percent'] < 0).sum())}"
        )

        print("\nAll query outputs match successfully!")

        print("\nReports saved successfully:")

        print(
            REPORT_DIR / "benchmark_results.csv"
        )

        print(
            REPORT_DIR / "query_plans.txt"
        )

        print("\nYottaFlex benchmark completed successfully!")

    finally:
        con.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_benchmarks(repetitions=7)
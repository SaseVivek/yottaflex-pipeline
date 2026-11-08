# YottaFlex AI – Data Pipeline Performance Optimization

A reproducible local data-engineering project using Python, DuckDB and SQL. The project generates deterministic synthetic e-commerce data, loads it into DuckDB staging tables, validates data quality, builds analytics tables, and compares baseline and optimized analytical SQL.

## Implemented components

- [x] Deterministic synthetic source data generation
- [x] DuckDB staging-table loader
- [x] Primary-key, null-key, referential-integrity and business-rule checks
- [x] Analytics dimensions, fact table and reporting marts
- [x] Baseline and optimized SQL workloads
- [x] Baseline-versus-optimized result reconciliation
- [x] Query timing and `EXPLAIN ANALYZE` plan capture
- [x] Automated transformation tests

**Important:** Benchmark timings depend on data volume, machine load, DuckDB version and cache state. A positive improvement percentage means the optimized query was faster in that run; a negative value means it was slower. Do not claim a speedup unless the measured report supports it.

## Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the project

Run commands from the repository root:

```powershell
# Generate deterministic synthetic source CSVs
python -m src.yottaflex.generate_data --scale 1 --seed 42

# Run data loading, quality checks and analytics transformations
python -m src.yottaflex.pipeline

# Run automated tests
pytest -v

# Compare baseline and optimized SQL queries
python -m src.yottaflex.benchmark

# Inspect benchmark results
Import-Csv .\reports\benchmark_results.csv | Format-Table -AutoSize
```

Use `--scale 50` for a larger run (over 100,000 total source rows across the generated tables).

## Project structure

- `src/yottaflex/` – pipeline, database, data generation, quality, transformation and benchmark modules
- `sql/baseline/` – original analytical SQL
- `sql/optimized/` – rewritten analytical SQL
- `tests/` – automated tests
- `data/raw/` – generated source CSV files
- `reports/` – benchmark CSV and query execution plans
- `docs/` – architecture notes

## Data and security

All generated records are synthetic. Do not add credentials, personal data or proprietary datasets to the public repository. The local DuckDB database and generated data are reproducible from the generator command.

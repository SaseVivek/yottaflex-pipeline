# YottaFlex AI – Data Pipeline Performance Optimization

<p align="center">
  <strong>A Reproducible Data Engineering Pipeline for Data Quality, Analytics Transformation, and SQL Performance Optimization</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" />
  <img src="https://img.shields.io/badge/Database-DuckDB-yellow" />
  <img src="https://img.shields.io/badge/SQL-Analytics-orange" />
  <img src="https://img.shields.io/badge/Testing-Pytest-green" />
  <img src="https://img.shields.io/badge/Status-Completed-success" />
</p>

---

## 1. Project Overview

**YottaFlex AI – Data Pipeline Performance Optimization** is a local, reproducible data engineering project designed to demonstrate how raw e-commerce data can be transformed into reliable, analytics-ready datasets through an automated data pipeline.

The project uses Python, DuckDB, and SQL to generate synthetic e-commerce data, load source files into staging tables, perform data quality validation, build analytical tables, and evaluate SQL query performance.

A key objective is to compare traditional baseline SQL queries with optimized SQL queries while ensuring that both approaches produce equivalent analytical results.

The project also captures query execution times and execution plans to provide measurable evidence of query performance.

### Key Objectives

- Build a reproducible end-to-end data pipeline.
- Generate deterministic synthetic e-commerce datasets.
- Load and manage structured data using DuckDB.
- Implement automated data quality validation.
- Transform staging data into analytics-ready tables.
- Develop baseline and optimized SQL queries.
- Measure and compare SQL query execution performance.
- Validate analytical results for correctness.
- Generate reports for performance analysis and verification.

---

## 2. Business Problem

E-commerce businesses generate large amounts of transactional data from customers, orders, products, order items, and payments.

However, raw data cannot always be used directly for business reporting because it may contain missing values, invalid records, inconsistent relationships, or incorrect business values.

Additionally, complex analytical SQL queries involving multiple joins and aggregations can increase query execution time.

This project addresses these challenges through two major areas:

**Data Engineering**
- Automated data generation and loading.
- Data quality validation.
- Structured transformations.
- Analytics table creation.

**Query Performance Optimization**
- Baseline SQL execution.
- Optimized SQL execution.
- Result reconciliation.
- Performance measurement.
- Execution plan analysis.

The objective is not simply to make queries faster, but to improve performance without changing the underlying business logic.

---

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline development and automation |
| DuckDB | Local analytical database |
| SQL | Data transformation and analytical queries |
| Pandas | Data handling and result comparison |
| NumPy | Numerical operations and synthetic data support |
| Pytest | Automated testing |
| Git & GitHub | Version control and project hosting |
| PowerShell | Local project execution |

### Main Python Libraries

- `pandas`
- `numpy`
- `duckdb`
- `pytest`
- `pathlib`
- `time`

---

## 4. Project Architecture

The project follows a structured data engineering workflow.

```text
             SYNTHETIC DATA GENERATION
                       |
                       v
                RAW CSV DATA
                       |
                       v
              DUCKDB DATA LOADING
                       |
                       v
                STAGING TABLES
                       |
                       v
               DATA QUALITY CHECKS
                       |
                       v
             ANALYTICS TRANSFORMATIONS
                       |
                       v
              ANALYTICS-READY TABLES
                       |
              +--------+--------+
              |                 |
              v                 v
        BASELINE SQL       OPTIMIZED SQL
              |                 |
              v                 v
        QUERY EXECUTION   QUERY EXECUTION
              |                 |
              +--------+--------+
                       |
                       v
              RESULT RECONCILIATION
                       |
                       v
              PERFORMANCE BENCHMARK
                       |
                       v
                REPORT GENERATION
```

### Pipeline Workflow

**Step 1 – Synthetic Data Generation**

Generate reproducible synthetic e-commerce source datasets using Python.

A fixed random seed ensures that the same input data can be generated again for repeatable testing.

**Step 2 – Data Loading**

Load generated CSV files into DuckDB staging tables.

**Step 3 – Data Quality Validation**

Validate the source data through automated checks, including:

- Primary-key uniqueness.
- Null-key detection.
- Referential-integrity validation.
- Business-rule validation.

**Step 4 – Analytics Transformation**

Transform staging data into structured analytical datasets, including dimensions, fact tables, and reporting marts.

**Step 5 – SQL Development**

Maintain two versions of analytical SQL workloads:

- Baseline queries representing the original implementation.
- Optimized queries using alternative SQL execution strategies.

**Step 6 – Result Reconciliation**

Execute both query versions and compare their output columns, row counts, and values.

**Step 7 – Performance Benchmarking**

Measure query execution time across multiple repetitions and calculate median execution time.

**Step 8 – Report Generation**

Save benchmark results and SQL execution plans for further analysis.

---

## 5. Data Engineering Components

### 5.1 Synthetic Data Generation

The project generates deterministic synthetic e-commerce data rather than depending on external datasets.

This makes the pipeline easier to reproduce, test, and execute locally.

Data generation supports configurable scale and random seed parameters.

Example:

```powershell
python -m src.yottaflex.generate_data --scale 1 --seed 42
```

For a larger dataset:

```powershell
python -m src.yottaflex.generate_data --scale 50 --seed 42
```

### 5.2 Data Loading

Generated CSV files are loaded into DuckDB staging tables.

The staging layer provides a structured starting point for validation and transformation operations.

### 5.3 Data Quality Checks

Data quality is an important part of the pipeline because incorrect source records can affect downstream analytics.

The project implements the following checks:

| Validation | Purpose |
|---|---|
| Primary-key checks | Identify duplicate key values |
| Null-key checks | Identify missing identifiers |
| Referential-integrity checks | Validate relationships between tables |
| Business-rule checks | Identify records that violate defined business conditions |

### 5.4 Analytics Transformations

The transformation layer builds analytical structures from the staging tables.

Implemented analytical components include:

- Dimension tables.
- Fact tables.
- Reporting marts.

These structures provide organized datasets for analytical SQL workloads and reporting.

---

## 6. SQL Performance Optimization

One of the main objectives of this project is to compare the performance of baseline and optimized SQL queries.

The same business requirements are implemented in both versions.

### Baseline SQL

Baseline queries use the original analytical SQL implementation.

They include joins, filtering, aggregations, grouping, and sorting operations.

### Optimized SQL

Optimized queries introduce alternative execution strategies where appropriate.

Techniques used include:

- Filtering completed orders before downstream joins.
- Pre-aggregating order-item data.
- Using Common Table Expressions (CTEs).
- Reducing repeated aggregation work.
- Preserving the original business logic.

### Query 1 – Revenue by Customer City and Product Category

**Business objective:**

Understand how much revenue is generated across different customer cities and product categories.

**Metrics:**
- Total revenue.
- Total quantity sold.
- Total distinct orders.

**Optimization approach:**

Aggregate order-item records before joining with customer and product information.

### Query 2 – Customer-wise Spending

**Business objective:**

Identify customer spending patterns and understand customer purchasing activity.

**Metrics:**
- Total orders.
- Total spending.
- Customer-wise spending distribution.

**Optimization approach:**

Pre-aggregate order-item spending at the order level before joining with customer and completed-order information.

### Query 3 – Payment Method Performance

**Business objective:**

Analyze payment activity across different payment methods and payment statuses.

**Metrics:**
- Payment count.
- Total payment amount.
- Average payment amount.

**Optimization approach:**

Preserve the original aggregation logic because DuckDB already optimizes this type of simple aggregation.

---

## 7. Benchmarking Methodology

The benchmarking module evaluates the execution performance of baseline and optimized SQL queries.

The benchmark process includes:

1. Load baseline and optimized SQL files.
2. Execute both query versions.
3. Compare their output datasets.
4. Perform a warm-up execution.
5. Execute each query multiple times.
6. Record execution durations.
7. Calculate median execution time.
8. Calculate percentage performance improvement.
9. Capture execution plans using `EXPLAIN ANALYZE`.
10. Save the final reports.

### Performance Improvement Formula

The percentage improvement is calculated using:

```text
Improvement (%) =

((Baseline Time - Optimized Time)
 / Baseline Time) × 100
```

**Interpretation:**

- Positive percentage: Optimized query executed faster.
- Negative percentage: Optimized query executed slower.
- Zero percentage: Both queries recorded approximately equal execution time.

### Result Validation

Performance alone is not sufficient.

Both query versions must return equivalent results.

The validation process checks:

- Column names.
- Number of records.
- Result values.
- Floating-point differences within defined tolerances.

This ensures that query optimization does not unintentionally change the analytical output.

### Benchmark Reports

The project generates two report files:

**1. benchmark_results.csv**

Contains:

| Column | Description |
|---|---|
| query_id | Query identification number |
| baseline_ms | Baseline execution time |
| optimized_ms | Optimized execution time |
| improvement_percent | Percentage performance improvement |
| results_match | Output validation status |
| baseline_rows | Baseline result row count |
| optimized_rows | Optimized result row count |

**2. query_plans.txt**

Contains execution plan information captured using DuckDB's `EXPLAIN ANALYZE`.

These plans help understand the operations performed during query execution.

**Important:** Performance measurements are environment-dependent. Actual results may vary based on dataset size, system resources, cache state, and DuckDB version. No optimization is guaranteed to improve every query.

---

## 8. Automated Testing

The project includes automated tests using Pytest to verify transformation functionality.

The test suite covers:

- Payment amount separation from revenue.
- Product revenue calculations.
- Customer lifetime value calculations.
- Daily sales calculations.

Run the test suite:

```powershell
python -m pytest -v
```

The current local verification recorded:

```text
7 passed
```

Successful test execution indicates that the tested transformation functions passed their defined test cases.

---

## 9. Project Directory Structure

```text
yottaflex_pipeline/
│
├── src/
│   └── yottaflex/
│       ├── __init__.py
│       ├── generate_data.py
│       ├── pipeline.py
│       ├── benchmark.py
│       ├── database.py
│       ├── quality.py
│       └── transform.py
│
├── sql/
│   ├── baseline/
│   │   └── baseline_queries.sql
│   │
│   └── optimized/
│       └── optimized_queries.sql
│
├── tests/
│   └── test_transform.py
│
├── data/
│   └── raw/
│       └── Generated CSV files
│
├── reports/
│   ├── benchmark_results.csv
│   └── query_plans.txt
│
├── docs/
│   └── prompt_history.md
│
├── README.md
├── requirements.txt
└── pytest.ini
```

*Note: The directory listing represents the intended project organization. Actual files depend on the final repository contents.*

---

## 10. Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.10 or later.
- Git.
- Visual Studio Code (recommended).

### Step 1 – Clone the Repository

```powershell
git clone https://github.com/SaseVivek/yottaflex-pipeline.git
```

### Step 2 – Navigate to the Project

```powershell
cd yottaflex-pipeline
```

### Step 3 – Create a Virtual Environment

```powershell
python -m venv .venv
```

### Step 4 – Activate the Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use the following command for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### Step 5 – Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

---

## 11. Running the Complete Project

Execute the following commands from the project root directory.

**Generate synthetic data:**

```powershell
python -m src.yottaflex.generate_data --scale 1 --seed 42
```

**Run the data pipeline:**

```powershell
python -m src.yottaflex.pipeline
```

**Execute automated tests:**

```powershell
python -m pytest -v
```

**Run SQL benchmarks:**

```powershell
python -m src.yottaflex.benchmark
```

**View benchmark results:**

```powershell
Import-Csv .\reports\benchmark_results.csv | Format-Table -AutoSize
```

**View query execution plans:**

```powershell
Get-Content .\reports\query_plans.txt
```

---

## 12. Results and Deliverables

The project produces the following outputs:

| Deliverable | Description |
|---|---|
| Synthetic datasets | Reproducible e-commerce source data |
| DuckDB staging tables | Loaded structured source records |
| Data quality validations | Checks for source data correctness |
| Analytics tables | Dimensions, fact tables and reporting marts |
| Baseline SQL queries | Original analytical queries |
| Optimized SQL queries | Alternative SQL implementations |
| Benchmark CSV | Query execution performance results |
| Query plans | DuckDB execution plan details |
| Automated tests | Transformation validation |

### Verified Local Execution

The following results were observed during local project validation:

- Benchmark script completed successfully.
- All three baseline and optimized query outputs matched.
- Seven automated tests passed.
- Benchmark results were generated.
- Query execution plans were generated.

---

## 13. Design Decisions

### Why DuckDB?

DuckDB provides a lightweight analytical database that can run locally without requiring a separate database server.

It is suitable for reproducible analytical workloads and SQL performance experiments.

### Why Synthetic Data?

Synthetic data allows the project to generate consistent datasets without relying on external or confidential business information.

### Why Separate Baseline and Optimized Queries?

Maintaining separate SQL implementations makes performance comparisons easier and allows the original business logic to be checked against the optimized version.

### Why Median Execution Time?

Median execution time reduces the influence of unusually slow or fast individual executions compared with relying on a single measurement.

### Why Automated Validation?

Query optimization must preserve analytical correctness. Comparing outputs helps identify changes that could otherwise produce incorrect reporting results.

---

## 14. Limitations and Future Enhancements

### Current Limitations

- Benchmark timings are dependent on the local execution environment.
- Synthetic data may not represent every real-world e-commerce scenario.
- Query optimization benefits can vary by query and dataset size.
- The project focuses on local analytical processing rather than distributed production infrastructure.

### Future Enhancements

- Introduce larger and more diverse datasets.
- Add incremental data loading.
- Implement additional data quality metrics.
- Explore partitioning and indexing strategies where appropriate.
- Add automated benchmark comparison across dataset scales.
- Introduce pipeline monitoring and structured logging.
- Integrate a BI dashboard for analytical reporting.
- Add CI workflows for automated testing.

---

## 15. AI Assistance and Transparency

AI tools were used as development assistance during this project.

AI assistance covered:

- Understanding project requirements.
- Exploring SQL optimization approaches.
- Developing and reviewing Python benchmark logic.
- Troubleshooting execution and testing issues.
- Improving documentation and project organization.

The generated suggestions and code were reviewed, integrated, executed, and validated as part of the development process.

The project includes `docs/prompt_history.md` to document AI prompts and development assistance.

The developer remains responsible for understanding the implementation, verifying correctness, and explaining the final technical decisions.

---

## 16. Repository

**GitHub Repository:**

https://github.com/SaseVivek/yottaflex-pipeline

---

## 17. Author

**Vivek Sase**

GitHub: https://github.com/SaseVivek

---

## Conclusion

YottaFlex AI demonstrates a complete local data engineering workflow, starting from synthetic data generation and ending with analytics-ready datasets and SQL performance evaluation.

By combining Python automation, DuckDB, SQL transformations, data quality validation, automated testing, and query benchmarking, the project demonstrates practical data engineering concepts with an emphasis on reproducibility, correctness, and performance measurement.

The main principle behind this implementation is:

**Optimize for performance without compromising data correctness.**

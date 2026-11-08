# YottaFlex AI – Prompt History

## 1. Project Understanding and Implementation

**Prompt 1:**
Help me understand the YottaFlex AI project requirements. Analyze the expected deliverables and explain the project architecture, implementation steps, technologies, and execution workflow.

**Prompt 2:**
Help me implement a complete, executable data pipeline project using Python, SQL, and DuckDB. Organize the project into modular components with proper folder structure, configuration, logging, and error handling.

## 2. SQL Development and Optimization

**Prompt 3:**
Create baseline SQL queries for the YottaFlex AI project to analyze revenue by customer city and product category, customer-wise spending, and payment method performance.

**Prompt 4:**
Create optimized versions of the baseline SQL queries. Use suitable techniques such as filtering, pre-aggregation, and Common Table Expressions (CTEs), while preserving the original business logic and output.

**Prompt 5:**
Compare baseline and optimized SQL queries. Ensure both versions return identical results, including column names, row counts, and values.

## 3. Benchmarking and Performance Analysis

**Prompt 6:**
Develop a complete benchmark.py script to execute baseline and optimized SQL queries using DuckDB. Measure execution time, perform warm-up executions, calculate median execution time, and calculate performance improvement percentages.

**Prompt 7:**
Add result validation to the benchmark script using pandas. Compare both query outputs while allowing small floating-point differences.

**Prompt 8:**
Capture SQL execution plans using EXPLAIN ANALYZE and save benchmark results into CSV and execution plans into a text report inside the reports directory.

**Prompt 9:**
Generate a clear benchmark summary showing baseline execution time, optimized execution time, percentage improvement, result matching status, and row counts.

## 4. Debugging and Error Handling

**Prompt 10:**
Debug the DuckDB SQL parser error occurring while executing optimized SQL queries. Identify the issue and correct the SQL query-loading and execution logic.

**Prompt 11:**
Resolve Python module import errors such as ModuleNotFoundError: No module named 'src'. Explain the correct project execution commands and Python path configuration.

**Prompt 12:**
Help resolve pytest collection errors and configure the project so that all test modules can import the required project functions correctly.

**Prompt 13:**
Review the complete project for errors, incorrect paths, missing dependencies, SQL execution issues, and configuration problems. Provide corrections without breaking existing functionality.

## 5. Testing and Validation

**Prompt 14:**
Review the project's test cases and ensure that the transformation functions work correctly. Execute the test suite and explain any failures.

**Prompt 15:**
Validate the payment amount separation from revenue, product revenue, customer lifetime value, and daily sales calculations.

**Prompt 16:**
Verify the complete pipeline and benchmark execution. Confirm that all tests pass and baseline and optimized query outputs match.

## 6. Documentation and Submission

**Prompt 17:**
Create a professional README.md explaining the project overview, objectives, technology stack, folder structure, installation, dependencies, execution steps, testing, and benchmark results.

**Prompt 18:**
Document the project architecture, SQL optimization techniques, design decisions, assumptions, limitations, and performance evaluation.

**Prompt 19:**
Explain how to save all project files, exclude unnecessary virtual environment files, and create a ZIP archive for final submission.

**Prompt 20:**
Help initialize a Git repository, create meaningful commits, configure the GitHub remote repository, and push the complete project to a public GitHub repository.

## 7. Final Review

**Prompt 21:**
Perform a final review of the YottaFlex AI project against the submission requirements. Check executable code, public GitHub repository, README documentation, test coverage, benchmark reports, SQL correctness, and reproducibility.

**Prompt 22:**
Prepare a final submission checklist and identify any missing deliverables before submitting the project.

---

## AI Usage Disclosure

AI tools were used as development assistance during this project.

**Areas where AI assistance was used:**
- Understanding project requirements and implementation workflow.
- SQL query development and optimization suggestions.
- Benchmark script development and performance calculations.
- Debugging Python imports, SQL execution, and testing issues.
- Documentation, README preparation, and GitHub workflow guidance.

**My personal contribution and responsibility:**
- Reviewed the generated code and integrated it into the project.
- Configured and executed the pipeline locally.
- Investigated and resolved execution and import errors.
- Ran the benchmark and verified the generated reports.
- Executed the test suite and confirmed that all 7 tests passed.
- Verified that baseline and optimized SQL query outputs matched.
- Created the public GitHub repository and pushed the project.

**Validation Evidence:**
- Benchmark execution completed successfully.
- All 7 automated tests passed.
- All 3 baseline and optimized SQL query outputs matched.
- Benchmark results were saved in `reports/benchmark_results.csv`.
- Execution plans were saved in `reports/query_plans.txt`.



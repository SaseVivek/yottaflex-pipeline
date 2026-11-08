# Architecture and Design Notes

## Objective
Build a local, reproducible analytical pipeline and demonstrate measurable query-performance improvements without changing analytical results.

## Data model and grain
- customers: one row per customer (`customer_id`).
- products: one row per product (`product_id`).
- orders: one row per order (`order_id`).
- order_items: one row per order line (`order_item_id`).
- payments: one row per payment (`payment_id`); the initial generator creates one payment per order.

## Pipeline stages
1. Generate deterministic synthetic CSV files using a fixed random seed.
2. Load CSV files into DuckDB staging tables.
3. Run schema, key, referential-integrity and business-rule checks.
4. Execute baseline analytical SQL and record timing/profile information.
5. Execute optimized SQL and reconcile result sets.
6. Write run metadata, quality findings and performance reports.

## Initial assumptions
- The workload is an e-commerce reporting workload because the supplied brief does not prescribe a business domain in the visible problem statement.
- All generated data is synthetic.
- The initial generator uses a single payment row per order; later edge-case fixtures will test duplicate and invalid references separately.
- Performance comparisons must use the same data, database environment, query result and measurement method.

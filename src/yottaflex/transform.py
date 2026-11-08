
from __future__ import annotations

import duckdb


def build_analytics_tables(con: duckdb.DuckDBPyConnection):
    """Build analytical tables from validated staging data."""

    queries = [

        # Customer dimension
        """
        CREATE OR REPLACE TABLE dim_customers AS
        SELECT
            customer_id,
            customer_name,
            city,
            region,
            signup_date
        FROM stg_customers
        """,

        # Product dimension
        """
        CREATE OR REPLACE TABLE dim_products AS
        SELECT
            product_id,
            product_name,
            category,
            unit_price
        FROM stg_products
        """,

        # Order-level fact table
        """
        CREATE OR REPLACE TABLE fact_orders AS
        WITH item_summary AS (
            SELECT
                order_id,
                SUM(quantity) AS total_quantity,
                SUM(line_amount) AS order_amount
            FROM stg_order_items
            GROUP BY order_id
        ),
        payment_summary AS (
            SELECT
                order_id,
                SUM(amount) AS total_payment_amount,
                COUNT(*) AS payment_count
            FROM stg_payments
            GROUP BY order_id
        )
        SELECT
            o.order_id,
            o.customer_id,
            o.order_date,
            o.order_status,
            COALESCE(i.total_quantity, 0) AS total_quantity,
            COALESCE(i.order_amount, 0) AS order_amount,
            COALESCE(p.total_payment_amount, 0)
                AS total_payment_amount,
            COALESCE(p.payment_count, 0) AS payment_count
        FROM stg_orders o
        LEFT JOIN item_summary i
            ON o.order_id = i.order_id
        LEFT JOIN payment_summary p
            ON o.order_id = p.order_id
        """,

        # Daily sales mart
        """
        CREATE OR REPLACE TABLE mart_daily_sales AS
        SELECT
            order_date,
            COUNT(*) AS total_orders,
            SUM(order_amount) AS total_sales,
            AVG(order_amount) AS average_order_value
        FROM fact_orders
        GROUP BY order_date
        ORDER BY order_date
        """,

        # Product performance mart
        """
        CREATE OR REPLACE TABLE mart_product_performance AS
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            SUM(oi.quantity) AS total_units_sold,
            SUM(oi.line_amount) AS total_revenue
        FROM stg_order_items oi
        JOIN dim_products p
            ON oi.product_id = p.product_id
        GROUP BY
            p.product_id,
            p.product_name,
            p.category
        """,

        # Customer analytics mart
        """
        CREATE OR REPLACE TABLE mart_customer_summary AS
        SELECT
            c.customer_id,
            c.customer_name,
            c.city,
            c.region,
            COUNT(o.order_id) AS total_orders,
            COALESCE(SUM(o.order_amount), 0) AS lifetime_value
        FROM dim_customers c
        LEFT JOIN fact_orders o
            ON c.customer_id = o.customer_id
        GROUP BY
            c.customer_id,
            c.customer_name,
            c.city,
            c.region
        """
    ]

    for query in queries:
        con.execute(query)

    print("Analytics transformation completed successfully!")

    return con.execute("""
        SHOW TABLES
    """).fetchdf()

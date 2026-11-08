
import duckdb
import pytest

from src.yottaflex.transform import build_analytics_tables


@pytest.fixture
def con():
    """Create an isolated in-memory DuckDB database."""

    connection = duckdb.connect(":memory:")

    connection.execute("""
        CREATE TABLE stg_customers (
            customer_id BIGINT,
            customer_name VARCHAR,
            city VARCHAR,
            region VARCHAR,
            signup_date DATE
        )
    """)

    connection.execute("""
        CREATE TABLE stg_products (
            product_id BIGINT,
            product_name VARCHAR,
            category VARCHAR,
            unit_price DOUBLE
        )
    """)

    connection.execute("""
        CREATE TABLE stg_orders (
            order_id BIGINT,
            customer_id BIGINT,
            order_date DATE,
            order_status VARCHAR
        )
    """)

    connection.execute("""
        CREATE TABLE stg_order_items (
            order_item_id BIGINT,
            order_id BIGINT,
            product_id BIGINT,
            quantity BIGINT,
            unit_price DOUBLE,
            line_amount DOUBLE
        )
    """)

    connection.execute("""
        CREATE TABLE stg_payments (
            payment_id BIGINT,
            order_id BIGINT,
            payment_method VARCHAR,
            payment_status VARCHAR,
            amount DOUBLE
        )
    """)

    # Sample customers
    connection.execute("""
        INSERT INTO stg_customers VALUES
        (1, 'Amit', 'Pune', 'West', '2026-01-01'),
        (2, 'Neha', 'Mumbai', 'West', '2026-01-02')
    """)

    # Sample products
    connection.execute("""
        INSERT INTO stg_products VALUES
        (101, 'Laptop', 'Electronics', 50000),
        (102, 'Mouse', 'Accessories', 1000)
    """)

    # Sample orders
    connection.execute("""
        INSERT INTO stg_orders VALUES
        (1001, 1, '2026-02-01', 'Completed'),
        (1002, 2, '2026-02-02', 'Completed')
    """)

    # Sample order items
    connection.execute("""
        INSERT INTO stg_order_items VALUES
        (1, 1001, 101, 1, 50000, 50000),
        (2, 1001, 102, 2, 1000, 2000),
        (3, 1002, 102, 1, 1000, 1000)
    """)

    # Sample payments
    connection.execute("""
        INSERT INTO stg_payments VALUES
        (1, 1001, 'UPI', 'Success', 52000),
        (2, 1002, 'Card', 'Success', 1000)
    """)

    yield connection
    connection.close()


def test_analytics_tables_created(con):
    build_analytics_tables(con)

    tables = con.execute("SHOW TABLES").fetchdf()["name"].tolist()

    expected = [
        "dim_customers",
        "dim_products",
        "fact_orders",
        "mart_daily_sales",
        "mart_product_performance",
        "mart_customer_summary"
    ]

    for table in expected:
        assert table in tables


def test_customer_count(con):
    build_analytics_tables(con)

    count = con.execute(
        "SELECT COUNT(*) FROM dim_customers"
    ).fetchone()[0]

    assert count == 2


def test_order_amount_calculation(con):
    build_analytics_tables(con)

    amount = con.execute("""
        SELECT order_amount
        FROM fact_orders
        WHERE order_id = 1001
    """).fetchone()[0]

    assert amount == pytest.approx(52000)


def test_payment_amount_separate_from_revenue(con):
    build_analytics_tables(con)

    result = con.execute("""
        SELECT order_amount, total_payment_amount
        FROM fact_orders
        WHERE order_id = 1001
    """).fetchone()

    assert result[0] == pytest.approx(52000)
    assert result[1] == pytest.approx(52000)


def test_product_revenue(con):
    build_analytics_tables(con)

    revenue = con.execute("""
        SELECT total_revenue
        FROM mart_product_performance
        WHERE product_id = 101
    """).fetchone()[0]

    assert revenue == pytest.approx(50000)


def test_customer_lifetime_value(con):
    build_analytics_tables(con)

    value = con.execute("""
        SELECT lifetime_value
        FROM mart_customer_summary
        WHERE customer_id = 1
    """).fetchone()[0]

    assert value == pytest.approx(52000)


def test_daily_sales(con):
    build_analytics_tables(con)

    result = con.execute("""
        SELECT total_orders, total_sales
        FROM mart_daily_sales
        WHERE order_date = '2026-02-01'
    """).fetchone()

    assert result[0] == 1
    assert result[1] == pytest.approx(52000)

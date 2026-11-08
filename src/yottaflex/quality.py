
from __future__ import annotations

from .database import connect


def run_quality_checks(con):
    """Run data quality checks on all staging tables."""

    results = []

    def check(name, query):
        count = con.execute(query).fetchone()[0]

        results.append({
            "check_name": name,
            "failed_records": count,
            "status": "PASS" if count == 0 else "FAIL"
        })

    # 1. Primary key duplicate checks
    primary_keys = {
        "customers": "customer_id",
        "products": "product_id",
        "orders": "order_id",
        "order_items": "order_item_id",
        "payments": "payment_id"
    }

    for table, key in primary_keys.items():
        check(
            f"{table}_duplicate_{key}",
            f"""
            SELECT COUNT(*) FROM (
                SELECT {key}
                FROM stg_{table}
                GROUP BY {key}
                HAVING COUNT(*) > 1
            )
            """
        )

        check(
            f"{table}_null_{key}",
            f"""
            SELECT COUNT(*)
            FROM stg_{table}
            WHERE {key} IS NULL
            """
        )

    # 2. Foreign key checks
    check(
        "orders_invalid_customer",
        """
        SELECT COUNT(*)
        FROM stg_orders o
        LEFT JOIN stg_customers c
        ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """
    )

    check(
        "order_items_invalid_order",
        """
        SELECT COUNT(*)
        FROM stg_order_items i
        LEFT JOIN stg_orders o
        ON i.order_id = o.order_id
        WHERE o.order_id IS NULL
        """
    )

    check(
        "order_items_invalid_product",
        """
        SELECT COUNT(*)
        FROM stg_order_items i
        LEFT JOIN stg_products p
        ON i.product_id = p.product_id
        WHERE p.product_id IS NULL
        """
    )

    check(
        "payments_invalid_order",
        """
        SELECT COUNT(*)
        FROM stg_payments p
        LEFT JOIN stg_orders o
        ON p.order_id = o.order_id
        WHERE o.order_id IS NULL
        """
    )

    # 3. Business rule checks
    check(
        "products_invalid_price",
        """
        SELECT COUNT(*)
        FROM stg_products
        WHERE unit_price < 0
        """
    )

    check(
        "order_items_invalid_quantity",
        """
        SELECT COUNT(*)
        FROM stg_order_items
        WHERE quantity <= 0
        """
    )

    check(
        "order_items_invalid_amount",
        """
        SELECT COUNT(*)
        FROM stg_order_items
        WHERE unit_price < 0 OR line_amount < 0
        """
    )

    check(
        "payments_invalid_amount",
        """
        SELECT COUNT(*)
        FROM stg_payments
        WHERE amount < 0
        """
    )

    return results


if __name__ == "__main__":
    con = connect()

    try:
        results = run_quality_checks(con)

        for result in results:
            print(
                f"{result['status']} | "
                f"{result['check_name']} | "
                f"Failed records: {result['failed_records']}"
            )

        failed = sum(
            r["status"] == "FAIL" for r in results
        )

        print("\nTotal checks:", len(results))
        print("Failed checks:", failed)
        print("Passed checks:", len(results) - failed)

        if failed:
            raise SystemExit(1)

    finally:
        con.close()

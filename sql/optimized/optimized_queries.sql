
-- ==========================================
-- YottaFlex AI - Optimized SQL Queries
-- Database: DuckDB
-- ==========================================

-- QUERY 1: Revenue by city and category
-- Optimization: Aggregate order items before
-- joining with other tables.

WITH completed_orders AS (
    SELECT order_id, customer_id
    FROM stg_orders
    WHERE UPPER(order_status) = 'COMPLETED'
),

item_summary AS (
    SELECT
        oi.order_id,
        oi.product_id,
        SUM(oi.line_amount) AS total_revenue,
        SUM(oi.quantity) AS total_quantity
    FROM stg_order_items oi
    INNER JOIN completed_orders o
        ON oi.order_id = o.order_id
    GROUP BY
        oi.order_id,
        oi.product_id
)

SELECT
    c.city,
    p.category,
    SUM(i.total_revenue) AS total_revenue,
    SUM(i.total_quantity) AS total_quantity,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM completed_orders o
JOIN stg_customers c
    ON o.customer_id = c.customer_id
JOIN item_summary i
    ON o.order_id = i.order_id
JOIN stg_products p
    ON i.product_id = p.product_id
GROUP BY
    c.city,
    p.category
ORDER BY total_revenue DESC;


-- QUERY 2: Customer-wise spending
-- Optimization: Filter completed orders before
-- aggregating order items.

WITH completed_orders AS (
    SELECT order_id, customer_id
    FROM stg_orders
    WHERE UPPER(order_status) = 'COMPLETED'
),

order_summary AS (
    SELECT
        oi.order_id,
        SUM(oi.line_amount) AS total_spending
    FROM stg_order_items oi
    INNER JOIN completed_orders o
        ON oi.order_id = o.order_id
    GROUP BY oi.order_id
)

SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(os.total_spending) AS total_spending
FROM completed_orders o
JOIN stg_customers c
    ON o.customer_id = c.customer_id
JOIN order_summary os
    ON o.order_id = os.order_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.city
ORDER BY total_spending DESC;



-- QUERY 3: Payment method performance
-- Preserve the original business logic.
-- DuckDB already optimizes simple aggregations.

SELECT
    payment_method,
    payment_status,
    COUNT(*) AS payment_count,
    SUM(amount) AS total_payment_amount,
    AVG(amount) AS average_payment_amount
FROM stg_payments
WHERE amount > 0
GROUP BY
    payment_method,
    payment_status
ORDER BY total_payment_amount DESC;

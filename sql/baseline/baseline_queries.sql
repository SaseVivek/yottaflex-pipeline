
-- ==========================================
-- YottaFlex AI - Baseline SQL Queries
-- Purpose: Measure initial query performance
-- Database: DuckDB
-- ==========================================

-- QUERY 1: Revenue by customer city and
-- product category

SELECT
    c.city,
    p.category,
    SUM(oi.line_amount) AS total_revenue,
    SUM(oi.quantity) AS total_quantity,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM stg_customers c
JOIN stg_orders o
    ON c.customer_id = o.customer_id
JOIN stg_order_items oi
    ON o.order_id = oi.order_id
JOIN stg_products p
    ON oi.product_id = p.product_id
WHERE UPPER(o.order_status) = 'COMPLETED'
GROUP BY
    c.city,
    p.category
ORDER BY total_revenue DESC;


-- QUERY 2: Customer-wise spending

SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.line_amount) AS total_spending
FROM stg_customers c
JOIN stg_orders o
    ON c.customer_id = o.customer_id
JOIN stg_order_items oi
    ON o.order_id = oi.order_id
WHERE UPPER(o.order_status) = 'COMPLETED'
GROUP BY
    c.customer_id,
    c.customer_name,
    c.city
ORDER BY total_spending DESC;


-- QUERY 3: Payment method performance

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

CREATE OR REPLACE VIEW ecommerce.order_status_summary AS
SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM ecommerce.fact_orders
GROUP BY order_status
ORDER BY total_orders DESC;
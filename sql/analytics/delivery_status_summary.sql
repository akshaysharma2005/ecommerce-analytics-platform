CREATE OR REPLACE VIEW ecommerce.delivery_status_summary AS
SELECT
    delivery_status,
    COUNT(*) AS total_orders,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM ecommerce.delivery_performance
GROUP BY delivery_status
ORDER BY total_orders DESC;
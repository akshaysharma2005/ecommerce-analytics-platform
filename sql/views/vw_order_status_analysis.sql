CREATE OR REPLACE VIEW ecommerce.vw_order_status_analysis AS

SELECT
    order_status,

    COUNT(DISTINCT order_id) AS total_orders,

    COUNT(DISTINCT customer_key) AS unique_customers,

    COUNT(DISTINCT order_id)
        FILTER (WHERE order_status = 'delivered')
        AS delivered_orders,

    ROUND(
        100.0 * COUNT(DISTINCT order_id)
        FILTER (WHERE order_status = 'delivered')
        / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS delivered_percentage

FROM ecommerce.fact_orders

GROUP BY
    order_status

ORDER BY
    total_orders DESC;
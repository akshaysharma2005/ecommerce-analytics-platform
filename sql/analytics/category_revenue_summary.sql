CREATE OR REPLACE VIEW ecommerce.customer_revenue_summary AS

SELECT
    customer_unique_id,

    COUNT(DISTINCT order_id) AS total_orders,

    COUNT(*) AS total_items,

    ROUND(SUM(price), 2) AS product_revenue,

    ROUND(SUM(freight_value), 2) AS freight_revenue,

    ROUND(SUM(total_item_value), 2) AS total_customer_spending,

    ROUND(AVG(total_item_value), 2) AS average_item_value,

    MIN(order_date) AS first_order_date,

    MAX(order_date) AS last_order_date

FROM ecommerce.vw_order_revenue

GROUP BY
    customer_unique_id

ORDER BY
    total_customer_spending DESC;
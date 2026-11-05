CREATE OR REPLACE VIEW ecommerce.monthly_revenue_summary AS
SELECT
    year,
    month,
    month_name,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items,
    ROUND(SUM(price), 2) AS product_revenue,
    ROUND(SUM(freight_value), 2) AS freight_revenue,
    ROUND(SUM(total_item_value), 2) AS total_revenue,
    ROUND(AVG(total_item_value), 2) AS average_item_value
FROM ecommerce.vw_order_revenue
GROUP BY
    year,
    month,
    month_name
ORDER BY
    year,
    month;
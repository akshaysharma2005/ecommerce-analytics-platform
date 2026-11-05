CREATE OR REPLACE VIEW ecommerce.vw_monthly_revenue AS

SELECT
    year,
    month,
    month_name,

    COUNT(DISTINCT order_id) AS total_orders,

    COUNT(*) AS total_items,

    SUM(price) AS total_product_revenue,

    SUM(freight_value) AS total_freight,

    SUM(total_item_value) AS total_revenue,

    AVG(total_item_value) AS average_item_value

FROM ecommerce.vw_order_revenue

GROUP BY
    year,
    month,
    month_name

ORDER BY
    year,
    month;
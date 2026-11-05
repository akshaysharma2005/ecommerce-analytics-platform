CREATE OR REPLACE VIEW ecommerce.vw_customer_revenue AS

SELECT
    customer_unique_id,

    COUNT(DISTINCT order_id) AS total_orders,

    COUNT(*) AS total_items,

    SUM(price) AS total_product_revenue,

    SUM(freight_value) AS total_freight,

    SUM(total_item_value) AS total_revenue,

    AVG(total_item_value) AS average_order_item_value,

    MIN(order_date) AS first_order_date,

    MAX(order_date) AS last_order_date

FROM ecommerce.vw_order_revenue

GROUP BY
    customer_unique_id;
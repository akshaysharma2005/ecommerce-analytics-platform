CREATE OR REPLACE VIEW ecommerce.seller_revenue_summary AS
SELECT
    seller_key,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items,
    ROUND(SUM(price), 2) AS product_revenue,
    ROUND(SUM(freight_value), 2) AS freight_revenue,
    ROUND(SUM(total_item_value), 2) AS total_revenue,
    ROUND(AVG(price), 2) AS average_product_price,
    ROUND(AVG(freight_value), 2) AS average_freight
FROM ecommerce.vw_order_revenue
GROUP BY seller_key
ORDER BY total_revenue DESC;
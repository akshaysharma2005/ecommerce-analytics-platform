CREATE OR REPLACE VIEW ecommerce.vw_product_revenue AS

SELECT
    product_key,
    product_category_name,
    product_category_name_english,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items,
    SUM(price) AS total_product_revenue,
    SUM(freight_value) AS total_freight,
    SUM(total_item_value) AS total_revenue,
    AVG(price) AS average_product_price,
    AVG(freight_value) AS average_freight

FROM ecommerce.vw_order_revenue

GROUP BY
    product_key,
    product_category_name,
    product_category_name_english;
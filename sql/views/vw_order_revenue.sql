CREATE OR REPLACE VIEW ecommerce.vw_order_revenue AS

SELECT
    fo.order_id,
    fo.customer_key,
    dc.customer_unique_id,

    fo.order_status,
    dd.full_date AS order_date,
    dd.year,
    dd.quarter,
    dd.month,
    dd.month_name,

    oi.order_item_id,
    oi.product_key,
    dp.product_category_name,
    dp.product_category_name_english,

    oi.seller_key,

    oi.price,
    oi.freight_value,
    oi.item_total_value,

    oi.price + oi.freight_value AS total_item_value

FROM ecommerce.fact_orders fo

JOIN ecommerce.fact_order_items oi
    ON fo.order_id = oi.order_id

JOIN ecommerce.dim_customer dc
    ON fo.customer_key = dc.customer_key

JOIN ecommerce.dim_product dp
    ON oi.product_key = dp.product_key

JOIN ecommerce.dim_date dd
    ON fo.purchase_date_key = dd.date_key;
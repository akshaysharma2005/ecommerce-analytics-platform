DROP VIEW IF EXISTS ecommerce.customer_purchase_behavior;

CREATE VIEW ecommerce.customer_purchase_behavior AS

SELECT
    customer_unique_id,
    total_orders,
    total_items,
    ROUND(total_revenue, 2) AS total_revenue,

    ROUND(
        total_revenue / NULLIF(total_orders, 0),
        2
    ) AS average_order_value,

    first_order_date,
    last_order_date,

    CASE
        WHEN total_orders = 1
            THEN 'One-Time Customer'
        WHEN total_orders BETWEEN 2 AND 3
            THEN 'Repeat Customer'
        ELSE 'Loyal Customer'
    END AS customer_type

FROM ecommerce.vw_customer_revenue;
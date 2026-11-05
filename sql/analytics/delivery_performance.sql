-- ============================================================
-- DELIVERY PERFORMANCE ANALYSIS
-- ============================================================

CREATE OR REPLACE VIEW ecommerce.delivery_performance AS

SELECT
    order_id,
    customer_key,
    order_status,

    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date,

    CASE
        WHEN order_delivered_customer_date IS NOT NULL
        THEN
            order_delivered_customer_date::date
            - order_purchase_timestamp::date
    END AS delivery_days,

    CASE
        WHEN order_delivered_customer_date IS NOT NULL
        THEN
            order_delivered_customer_date::date
            - order_estimated_delivery_date::date
    END AS delivery_vs_estimated_days,

    CASE
        WHEN order_delivered_customer_date IS NOT NULL
             AND order_delivered_customer_date::date
                 <= order_estimated_delivery_date::date
        THEN 'On Time'

        WHEN order_delivered_customer_date IS NOT NULL
             AND order_delivered_customer_date::date
                 > order_estimated_delivery_date::date
        THEN 'Late'

        ELSE 'Not Delivered'
    END AS delivery_status

FROM ecommerce.fact_orders;
-- ============================================================
-- VIEW: vw_regional_revenue
-- Member 3: Product, Revenue & Marketing Analytics
-- Integrates customer geography with order revenue & freight
-- ============================================================

CREATE OR REPLACE VIEW ecommerce.vw_regional_revenue AS

SELECT
    dc.customer_state,

    CASE
        WHEN dc.customer_state IN ('SP', 'RJ', 'MG', 'ES') THEN 'Southeast'
        WHEN dc.customer_state IN ('PR', 'SC', 'RS') THEN 'South'
        WHEN dc.customer_state IN ('BA', 'PE', 'CE', 'MA', 'PB', 'RN', 'AL', 'PI', 'SE') THEN 'Northeast'
        WHEN dc.customer_state IN ('DF', 'GO', 'MT', 'MS') THEN 'Central-West'
        WHEN dc.customer_state IN ('AM', 'PA', 'RO', 'TO', 'AC', 'AP', 'RR') THEN 'North'
        ELSE 'Other'
    END AS macro_region,

    COUNT(DISTINCT fo.order_id) AS total_orders,
    COUNT(DISTINCT dc.customer_unique_id) AS unique_customers,
    COUNT(oi.order_item_id) AS total_items,

    ROUND(SUM(oi.price), 2) AS product_revenue,
    ROUND(SUM(oi.freight_value), 2) AS freight_revenue,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,

    ROUND(AVG(oi.price + oi.freight_value), 2) AS average_item_value,
    ROUND(SUM(oi.price + oi.freight_value) / NULLIF(COUNT(DISTINCT fo.order_id), 0), 2) AS average_order_value,
    ROUND(SUM(oi.price + oi.freight_value) / NULLIF(COUNT(DISTINCT dc.customer_unique_id), 0), 2) AS spend_per_customer,

    ROUND(100.0 * SUM(oi.freight_value) / NULLIF(SUM(oi.price + oi.freight_value), 0), 2) AS freight_share_pct

FROM ecommerce.fact_orders fo

JOIN ecommerce.dim_customer dc
    ON fo.customer_key = dc.customer_key

JOIN ecommerce.fact_order_items oi
    ON fo.order_id = oi.order_id

GROUP BY
    dc.customer_state,
    macro_region;


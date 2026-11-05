-- ============================================================
-- VIEW: vw_returns_analysis
-- Member 3: Product, Revenue & Marketing Analytics
-- Integrates fact_returns, dim_product, dim_customer, dim_seller
-- ============================================================

CREATE OR REPLACE VIEW ecommerce.vw_returns_analysis AS

SELECT
    fr.return_key,
    fr.return_id,
    fr.order_id,
    fr.order_item_id,
    fr.return_date,
    dd.year AS return_year,
    dd.month AS return_month,
    dd.month_name AS return_month_name,

    fr.return_type,
    fr.return_reason,
    fr.is_damaged_or_defective,

    fr.product_key,
    dp.product_id,
    COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown') AS product_category_name,

    fr.seller_key,
    ds.seller_id,
    ds.seller_state,

    fr.customer_key,
    dc.customer_unique_id,
    dc.customer_state,

    fr.refund_amount,
    fr.refund_freight,
    fr.total_refund

FROM ecommerce.fact_returns fr

JOIN ecommerce.dim_date dd
    ON fr.return_date_key = dd.date_key

LEFT JOIN ecommerce.dim_product dp
    ON fr.product_key = dp.product_key

LEFT JOIN ecommerce.dim_seller ds
    ON fr.seller_key = ds.seller_key

LEFT JOIN ecommerce.dim_customer dc
    ON fr.customer_key = dc.customer_key;


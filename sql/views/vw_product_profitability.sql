-- ============================================================
-- VIEW: vw_product_profitability
-- Member 3: Product, Revenue & Marketing Analytics
-- Calculates revenue, estimated COGS, gross profit, return loss, and net margin
-- ============================================================

CREATE OR REPLACE VIEW ecommerce.vw_product_profitability AS

WITH product_sales AS (
    SELECT
        dp.product_key,
        dp.product_id,
        COALESCE(dp.product_category_name_english, dp.product_category_name, 'unknown') AS product_category_name,
        COALESCE(dcm.benchmark_gross_margin_pct, 0.30) AS benchmark_gross_margin_pct,
        COALESCE(dcm.marketplace_commission_pct, 0.14) AS marketplace_commission_pct,
        COUNT(DISTINCT oi.order_id) AS total_orders,
        COUNT(oi.order_item_id) AS total_units_sold,
        SUM(oi.price) AS total_product_revenue,
        SUM(oi.freight_value) AS total_freight,
        SUM(oi.price + oi.freight_value) AS total_revenue,
        AVG(oi.price) AS average_price,
        AVG(oi.freight_value) AS average_freight
    FROM ecommerce.dim_product dp
    JOIN ecommerce.fact_order_items oi
        ON dp.product_key = oi.product_key
    LEFT JOIN ecommerce.dim_category_margin dcm
        ON COALESCE(dp.product_category_name_english, dp.product_category_name, 'unknown') = dcm.category_name
    GROUP BY
        dp.product_key,
        dp.product_id,
        COALESCE(dp.product_category_name_english, dp.product_category_name, 'unknown'),
        dcm.benchmark_gross_margin_pct,
        dcm.marketplace_commission_pct
),
product_returns AS (
    SELECT
        product_key,
        COUNT(*) AS returned_units,
        SUM(total_refund) AS total_refund_amount
    FROM ecommerce.fact_returns
    GROUP BY product_key
)
SELECT
    ps.product_key,
    ps.product_id,
    ps.product_category_name,
    ps.benchmark_gross_margin_pct,
    ps.marketplace_commission_pct,

    ps.total_orders,
    ps.total_units_sold,
    ROUND(ps.total_product_revenue, 2) AS total_product_revenue,
    ROUND(ps.total_freight, 2) AS total_freight,
    ROUND(ps.total_revenue, 2) AS total_revenue,
    ROUND(ps.average_price, 2) AS average_price,
    ROUND(ps.average_freight, 2) AS average_freight,

    -- Estimated Cost of Goods Sold (COGS)
    ROUND(ps.total_product_revenue * (1.0 - ps.benchmark_gross_margin_pct), 2) AS estimated_cogs,

    -- Gross Profit
    ROUND(ps.total_product_revenue * ps.benchmark_gross_margin_pct, 2) AS gross_profit,

    -- Marketplace Commission Revenue
    ROUND(ps.total_product_revenue * ps.marketplace_commission_pct, 2) AS marketplace_commission_revenue,

    -- Return / Refund Drag
    COALESCE(pr.returned_units, 0) AS returned_units,
    ROUND(COALESCE(pr.total_refund_amount, 0), 2) AS total_refund_amount,
    ROUND(100.0 * COALESCE(pr.returned_units, 0) / NULLIF(ps.total_units_sold, 0), 2) AS return_rate_pct,

    -- Net Profit Contribution (Gross Profit - Refund Loss)
    ROUND((ps.total_product_revenue * ps.benchmark_gross_margin_pct) - COALESCE(pr.total_refund_amount, 0), 2) AS net_profit_contribution,

    -- Net Profit Margin %
    ROUND(100.0 * ((ps.total_product_revenue * ps.benchmark_gross_margin_pct) - COALESCE(pr.total_refund_amount, 0)) / NULLIF(ps.total_revenue, 0), 2) AS net_profit_margin_pct

FROM product_sales ps
LEFT JOIN product_returns pr
    ON ps.product_key = pr.product_key;


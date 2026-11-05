-- ============================================================
-- MEMBER 3: PRODUCT ANALYTICS
-- Script: category_performance_scorecard.sql
-- Comprehensive 360° Category Performance Scorecard:
-- 1. Sales & Revenue Metrics (Orders, Units, Revenue, AOV)
-- 2. Profitability & Margins (COGS, Gross Profit, Net Margin)
-- 3. Quality & Customer Satisfaction (Return Rate, Avg Review)
-- 4. Strategic Portfolio Classification (BCG Matrix Quadrant)
-- ============================================================

WITH category_sales AS (
    SELECT
        COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown') AS category,
        COUNT(DISTINCT oi.order_id) AS total_orders,
        COUNT(oi.order_item_id) AS total_units_sold,
        SUM(oi.price) AS product_revenue,
        SUM(oi.freight_value) AS freight_revenue,
        SUM(oi.price + oi.freight_value) AS total_revenue,
        AVG(oi.price) AS avg_product_price,
        AVG(oi.freight_value) AS avg_freight
    FROM ecommerce.fact_order_items oi
    JOIN ecommerce.dim_product dp
        ON oi.product_key = dp.product_key
    GROUP BY 1
),
category_returns AS (
    SELECT
        COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown') AS category,
        COUNT(*) AS returned_units,
        SUM(fr.total_refund) AS total_refund_amount
    FROM ecommerce.fact_returns fr
    LEFT JOIN ecommerce.dim_product dp
        ON fr.product_key = dp.product_key
    GROUP BY 1
),
category_reviews AS (
    SELECT
        COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown') AS category,
        ROUND(AVG(frv.review_score), 2) AS avg_review_score,
        COUNT(frv.review_score) AS total_reviews
    FROM ecommerce.fact_reviews frv
    JOIN ecommerce.fact_order_items oi
        ON frv.order_id = oi.order_id
    JOIN ecommerce.dim_product dp
        ON oi.product_key = dp.product_key
    GROUP BY 1
),
marketplace_total AS (
    SELECT SUM(total_revenue) AS grand_total_revenue FROM category_sales
),
scorecard AS (
    SELECT
        cs.category,
        cs.total_orders,
        cs.total_units_sold,
        ROUND(cs.total_revenue, 2) AS total_revenue,
        ROUND(100.0 * cs.total_revenue / m.grand_total_revenue, 2) AS revenue_share_pct,
        ROUND(cs.total_revenue / NULLIF(cs.total_orders, 0), 2) AS aov,
        ROUND(cs.avg_product_price, 2) AS avg_price,
        ROUND(cs.avg_freight, 2) AS avg_freight,

        -- Margins
        COALESCE(dcm.benchmark_gross_margin_pct, 0.30) AS gross_margin_rate,
        ROUND(cs.product_revenue * COALESCE(dcm.benchmark_gross_margin_pct, 0.30), 2) AS gross_profit,

        -- Returns
        COALESCE(cr.returned_units, 0) AS returned_units,
        ROUND(COALESCE(cr.total_refund_amount, 0), 2) AS total_refund_amount,
        ROUND(100.0 * COALESCE(cr.returned_units, 0) / NULLIF(cs.total_units_sold, 0), 2) AS return_rate_pct,

        -- Net Contribution
        ROUND(
            (cs.product_revenue * COALESCE(dcm.benchmark_gross_margin_pct, 0.30)) 
            - COALESCE(cr.total_refund_amount, 0), 
            2
        ) AS net_profit_contribution,

        ROUND(
            100.0 * ((cs.product_revenue * COALESCE(dcm.benchmark_gross_margin_pct, 0.30)) - COALESCE(cr.total_refund_amount, 0))
            / NULLIF(cs.total_revenue, 0),
            2
        ) AS net_profit_margin_pct,

        -- Quality
        COALESCE(crv.avg_review_score, 4.00) AS avg_review_score

    FROM category_sales cs
    CROSS JOIN marketplace_total m
    LEFT JOIN ecommerce.dim_category_margin dcm
        ON cs.category = dcm.category_name
    LEFT JOIN category_returns cr
        ON cs.category = cr.category
    LEFT JOIN category_reviews crv
        ON cs.category = crv.category
)
SELECT
    ROW_NUMBER() OVER (ORDER BY total_revenue DESC) AS rank,
    category,
    total_orders,
    total_units_sold,
    total_revenue,
    revenue_share_pct,
    aov,
    gross_profit,
    return_rate_pct,
    net_profit_contribution,
    net_profit_margin_pct,
    avg_review_score,
    CASE
        WHEN revenue_share_pct >= 5.0 AND avg_review_score >= 4.05 THEN 'Star (Core Leader)'
        WHEN revenue_share_pct >= 5.0 AND avg_review_score < 4.05 THEN 'Cash Cow (Volume Driver)'
        WHEN revenue_share_pct < 5.0 AND avg_review_score >= 4.15 AND return_rate_pct < 2.0 THEN 'Question Mark (High Potential)'
        ELSE 'Underperformer / Watchlist'
    END AS strategic_quadrant
FROM scorecard
ORDER BY rank
LIMIT 20;


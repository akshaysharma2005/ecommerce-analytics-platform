-- ============================================================
-- MEMBER 3: REVENUE ANALYTICS
-- Script: monthly_revenue_growth.sql
-- Computes:
-- 1. Monthly revenue breakdown (product, freight, total)
-- 2. Month-over-Month (MoM) revenue growth ($ and %)
-- 3. Year-over-Year (YoY) revenue growth
-- 4. 3-Month Moving Average revenue
-- 5. Cumulative revenue over time
-- ============================================================

WITH monthly_rev AS (
    SELECT
        year,
        month,
        TO_CHAR(TO_DATE(year || '-' || LPAD(month::text, 2, '0') || '-01', 'YYYY-MM-DD'), 'Mon YYYY') AS period_label,
        total_orders,
        total_items,
        total_product_revenue,
        total_freight,
        total_revenue,
        ROUND(total_revenue / NULLIF(total_orders, 0), 2) AS monthly_aov
    FROM ecommerce.vw_monthly_revenue
),
growth_calc AS (
    SELECT
        year,
        month,
        period_label,
        total_orders,
        total_items,
        total_product_revenue,
        total_freight,
        total_revenue,
        monthly_aov,

        -- Previous month revenue for MoM calculation
        LAG(total_revenue, 1) OVER (ORDER BY year, month) AS prev_month_revenue,

        -- MoM Absolute Growth
        ROUND(total_revenue - LAG(total_revenue, 1) OVER (ORDER BY year, month), 2) AS mom_revenue_growth_val,

        -- MoM Growth Rate %
        ROUND(
            100.0 * (total_revenue - LAG(total_revenue, 1) OVER (ORDER BY year, month)) 
            / NULLIF(LAG(total_revenue, 1) OVER (ORDER BY year, month), 0),
            2
        ) AS mom_growth_pct,

        -- Previous year revenue for YoY calculation (lag 12 months)
        LAG(total_revenue, 12) OVER (ORDER BY year, month) AS prev_year_revenue,

        -- YoY Growth Rate %
        ROUND(
            100.0 * (total_revenue - LAG(total_revenue, 12) OVER (ORDER BY year, month)) 
            / NULLIF(LAG(total_revenue, 12) OVER (ORDER BY year, month), 0),
            2
        ) AS yoy_growth_pct,

        -- 3-Month Rolling Average Revenue
        ROUND(
            AVG(total_revenue) OVER (
                ORDER BY year, month 
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ),
            2
        ) AS rolling_3m_avg_revenue,

        -- Cumulative Revenue to Date
        ROUND(
            SUM(total_revenue) OVER (
                ORDER BY year, month
            ),
            2
        ) AS cumulative_revenue

    FROM monthly_rev
)
SELECT
    year,
    month,
    period_label,
    total_orders,
    total_items,
    ROUND(total_product_revenue, 2) AS product_revenue,
    ROUND(total_freight, 2) AS freight_revenue,
    ROUND(total_revenue, 2) AS total_revenue,
    monthly_aov,
    mom_revenue_growth_val,
    mom_growth_pct,
    yoy_growth_pct,
    rolling_3m_avg_revenue,
    cumulative_revenue
FROM growth_calc
ORDER BY year, month;


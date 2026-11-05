-- ============================================================
-- MEMBER 3: MARKETING ANALYTICS
-- Script: marketing_spend_cac_roi.sql
-- Computes:
-- 1. Marketing Performance by Acquisition Channel
-- 2. Channel Spend Allocation, CAC, ROAS, and ROI %
-- 3. Monthly Spend & Blended CAC Trends vs AOV (2016-2018)
-- ============================================================

-- 1. CHANNEL-LEVEL ACQUISITION & PROFITABILITY SCORECARD
WITH channel_summary AS (
    SELECT
        dc.channel,
        SUM(fmp.impressions) AS total_impressions,
        SUM(fmp.clicks) AS total_clicks,
        SUM(fmp.marketing_spend) AS total_marketing_spend,
        SUM(fmp.orders) AS total_orders,
        SUM(fmp.attributed_revenue) AS total_attributed_revenue
    FROM ecommerce.dim_campaign dc
    JOIN ecommerce.fact_marketing_performance fmp
        ON dc.campaign_key = fmp.campaign_key
    GROUP BY dc.channel
),
grand_totals AS (
    SELECT
        SUM(total_marketing_spend) AS grand_spend,
        SUM(total_attributed_revenue) AS grand_revenue,
        SUM(total_orders) AS grand_orders
    FROM channel_summary
)
SELECT
    c.channel,
    ROUND(c.total_marketing_spend, 2) AS marketing_spend,
    ROUND(100.0 * c.total_marketing_spend / g.grand_spend, 2) AS spend_share_pct,
    c.total_orders,
    ROUND(100.0 * c.total_orders / g.grand_orders, 2) AS order_share_pct,
    ROUND(c.total_attributed_revenue, 2) AS attributed_revenue,
    ROUND(100.0 * c.total_attributed_revenue / g.grand_revenue, 2) AS revenue_share_pct,

    -- Unit Economics
    ROUND(c.total_marketing_spend / NULLIF(c.total_orders, 0), 2) AS cac,
    ROUND(c.total_attributed_revenue / NULLIF(c.total_orders, 0), 2) AS channel_aov,
    ROUND(100.0 * (c.total_marketing_spend / NULLIF(c.total_orders, 0)) / NULLIF(c.total_attributed_revenue / NULLIF(c.total_orders, 0), 0), 2) AS cac_to_aov_pct,

    -- Returns
    ROUND(c.total_attributed_revenue / NULLIF(c.total_marketing_spend, 0), 2) AS roas,
    ROUND(
        100.0 * ((c.total_attributed_revenue * 0.30) - c.total_marketing_spend) 
        / NULLIF(c.total_marketing_spend, 0), 
        2
    ) AS marketing_roi_pct

FROM channel_summary c
CROSS JOIN grand_totals g
ORDER BY c.total_attributed_revenue DESC;


-- 2. MONTHLY SPEND & BLENDED CAC TRENDS (2016-2018)
WITH monthly_mkt AS (
    SELECT
        fmp.year,
        fmp.month,
        dd.month_name,
        SUM(fmp.marketing_spend) AS monthly_spend,
        SUM(fmp.orders) AS monthly_orders,
        SUM(fmp.attributed_revenue) AS monthly_revenue
    FROM ecommerce.fact_marketing_performance fmp
    JOIN ecommerce.dim_date dd
        ON fmp.date_key = dd.date_key
    GROUP BY fmp.year, fmp.month, dd.month_name
)
SELECT
    m.year,
    m.month,
    m.month_name,
    ROUND(m.monthly_spend, 2) AS monthly_marketing_spend,
    m.monthly_orders,
    ROUND(m.monthly_revenue, 2) AS monthly_attributed_revenue,
    ROUND(m.monthly_spend / NULLIF(m.monthly_orders, 0), 2) AS blended_cac,
    ROUND(m.monthly_revenue / NULLIF(m.monthly_orders, 0), 2) AS monthly_aov,
    ROUND(100.0 * (m.monthly_spend / NULLIF(m.monthly_orders, 0)) / NULLIF(m.monthly_revenue / NULLIF(m.monthly_orders, 0), 0), 2) AS cac_to_aov_pct,
    ROUND(m.monthly_revenue / NULLIF(m.monthly_spend, 0), 2) AS monthly_roas
FROM monthly_mkt m
ORDER BY m.year, m.month;


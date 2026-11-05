 -- ============================================================
-- MEMBER 3: MARKETING ANALYTICS
-- Script: marketing_campaign_performance.sql
-- Computes:
-- 1. Campaign-by-Campaign Performance Funnel (Impressions -> Clicks -> Leads -> Orders)
-- 2. Efficiency Metrics (CTR, CPC, CVR)
-- 3. Revenue Attribution, ROAS, and ROI %
-- ============================================================

SELECT
    dc.campaign_id,
    dc.campaign_name,
    dc.channel,
    dc.campaign_type,
    SUM(fmp.impressions) AS total_impressions,
    SUM(fmp.clicks) AS total_clicks,
    ROUND(SUM(fmp.marketing_spend), 2) AS total_marketing_spend,
    SUM(fmp.leads) AS total_leads,
    SUM(fmp.orders) AS total_orders_acquired,
    ROUND(SUM(fmp.attributed_revenue), 2) AS total_attributed_revenue,

    -- Funnel Efficiency Rates
    ROUND(100.0 * SUM(fmp.clicks) / NULLIF(SUM(fmp.impressions), 0), 2) AS overall_ctr_pct,
    ROUND(SUM(fmp.marketing_spend) / NULLIF(SUM(fmp.clicks), 0), 2) AS avg_cpc,
    ROUND(100.0 * SUM(fmp.orders) / NULLIF(SUM(fmp.clicks), 0), 2) AS overall_cvr_pct,
    ROUND(SUM(fmp.marketing_spend) / NULLIF(SUM(fmp.orders), 0), 2) AS cac,

    -- Financial Return
    ROUND(SUM(fmp.attributed_revenue) / NULLIF(SUM(fmp.marketing_spend), 0), 2) AS roas,
    ROUND(
        100.0 * ((SUM(fmp.attributed_revenue) * 0.30) - SUM(fmp.marketing_spend)) 
        / NULLIF(SUM(fmp.marketing_spend), 0), 
        2
    ) AS marketing_roi_pct

FROM ecommerce.dim_campaign dc
JOIN ecommerce.fact_marketing_performance fmp
    ON dc.campaign_key = fmp.campaign_key
GROUP BY
    dc.campaign_id,
    dc.campaign_name,
    dc.channel,
    dc.campaign_type
ORDER BY total_attributed_revenue DESC;

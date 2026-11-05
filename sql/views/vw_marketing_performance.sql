-- ============================================================
-- VIEW: vw_marketing_performance
-- Member 3: Product, Revenue & Marketing Analytics
-- Integrates marketing performance fact with campaign dimension
-- ============================================================

CREATE OR REPLACE VIEW ecommerce.vw_marketing_performance AS

SELECT
    fmp.marketing_performance_key,
    dc.campaign_key,
    dc.campaign_id,
    dc.campaign_name,
    dc.channel,
    dc.campaign_type,
    dc.target_audience,

    fmp.date_key,
    fmp.year,
    fmp.month,
    dd.month_name,

    fmp.impressions,
    fmp.clicks,
    fmp.marketing_spend,
    fmp.leads,
    fmp.orders,
    fmp.attributed_revenue,

    fmp.cpc,
    fmp.ctr,
    fmp.cvr,
    fmp.cac,
    fmp.roas,
    fmp.roi_pct

FROM ecommerce.fact_marketing_performance fmp

JOIN ecommerce.dim_campaign dc
    ON fmp.campaign_key = dc.campaign_key

JOIN ecommerce.dim_date dd
    ON fmp.date_key = dd.date_key;


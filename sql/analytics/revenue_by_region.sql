-- ============================================================
-- MEMBER 3: REVENUE ANALYTICS
-- Script: revenue_by_region.sql
-- Computes:
-- 1. Brazilian State-Level Revenue Ranking (27 States)
-- 2. Macro-Region Aggregation & Revenue Contribution
-- 3. Regional Freight Cost Burden & Logistics Drag
-- 4. Customer Spending & AOV by Geography
-- ============================================================

-- 1. MACRO-REGION SUMMARY
WITH macro_summary AS (
    SELECT
        macro_region,
        SUM(total_orders) AS total_orders,
        SUM(unique_customers) AS unique_customers,
        SUM(total_items) AS total_items,
        SUM(product_revenue) AS product_revenue,
        SUM(freight_revenue) AS freight_revenue,
        SUM(total_revenue) AS total_revenue
    FROM ecommerce.vw_regional_revenue
    GROUP BY macro_region
),
macro_totals AS (
    SELECT SUM(total_revenue) AS grand_total_revenue FROM macro_summary
)
SELECT
    m.macro_region,
    m.total_orders,
    m.unique_customers,
    m.total_items,
    ROUND(m.product_revenue, 2) AS product_revenue,
    ROUND(m.freight_revenue, 2) AS freight_revenue,
    ROUND(m.total_revenue, 2) AS total_revenue,
    ROUND(100.0 * m.total_revenue / t.grand_total_revenue, 2) AS revenue_share_pct,
    ROUND(m.total_revenue / NULLIF(m.total_orders, 0), 2) AS regional_aov,
    ROUND(m.total_revenue / NULLIF(m.unique_customers, 0), 2) AS spend_per_customer,
    ROUND(100.0 * m.freight_revenue / NULLIF(m.total_revenue, 0), 2) AS freight_share_pct,
    ROUND(m.freight_revenue / NULLIF(m.total_orders, 0), 2) AS avg_freight_per_order
FROM macro_summary m
CROSS JOIN macro_totals t
ORDER BY m.total_revenue DESC;


-- 2. STATE-LEVEL REVENUE RANKING (TOP 15 STATES)
WITH state_totals AS (
    SELECT
        customer_state,
        macro_region,
        total_orders,
        unique_customers,
        total_items,
        product_revenue,
        freight_revenue,
        total_revenue,
        average_order_value,
        spend_per_customer,
        freight_share_pct
    FROM ecommerce.vw_regional_revenue
),
state_grand AS (
    SELECT SUM(total_revenue) AS grand_total FROM state_totals
)
SELECT
    ROW_NUMBER() OVER (ORDER BY s.total_revenue DESC) AS rank,
    s.customer_state,
    s.macro_region,
    s.total_orders,
    s.unique_customers,
    ROUND(s.product_revenue, 2) AS product_revenue,
    ROUND(s.freight_revenue, 2) AS freight_revenue,
    ROUND(s.total_revenue, 2) AS total_revenue,
    ROUND(100.0 * s.total_revenue / g.grand_total, 2) AS state_revenue_share_pct,
    ROUND(
        100.0 * SUM(s.total_revenue) OVER (ORDER BY s.total_revenue DESC) / g.grand_total,
        2
    ) AS cumulative_share_pct,
    s.average_order_value,
    s.spend_per_customer,
    s.freight_share_pct
FROM state_totals s
CROSS JOIN state_grand g
ORDER BY rank
LIMIT 15;


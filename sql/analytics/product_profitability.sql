-- ============================================================
-- MEMBER 3: PRODUCT ANALYTICS
-- Script: product_profitability.sql
-- Computes:
-- 1. Top 15 Most Profitable Products (by Net Profit Contribution)
-- 2. Gross Profit vs Estimated COGS vs Return Loss
-- 3. Net Margin Percentage Contribution
-- ============================================================

SELECT
    ROW_NUMBER() OVER (ORDER BY net_profit_contribution DESC) AS rank,
    product_key,
    product_id,
    product_category_name AS category,
    total_orders,
    total_units_sold,
    total_revenue,
    estimated_cogs,
    gross_profit,
    returned_units,
    total_refund_amount,
    net_profit_contribution,
    net_profit_margin_pct
FROM ecommerce.vw_product_profitability
WHERE total_units_sold >= 10
ORDER BY net_profit_contribution DESC
LIMIT 15;


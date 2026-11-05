-- ============================================================
-- MEMBER 3: PRODUCT ANALYTICS
-- Script: return_heavy_products.sql
-- Computes:
-- 1. Top 15 Products with Highest Return / Cancellation Rate (%)
-- 2. Top 15 Products by Absolute Refund Value (BRL)
-- 3. Return Reasons Breakdown
-- 4. Overall Marketplace Return & Cancellation Benchmark
-- ============================================================

-- 1. TOP 15 PRODUCTS BY RETURN RATE % (Minimum 10 units sold)
SELECT
    ROW_NUMBER() OVER (ORDER BY vp.return_rate_pct DESC, vp.returned_units DESC) AS rank,
    vp.product_key,
    vp.product_id,
    vp.product_category_name AS category,
    vp.total_orders,
    vp.total_units_sold,
    vp.returned_units,
    vp.return_rate_pct,
    vp.total_refund_amount,
    vp.total_revenue,
    ROUND(100.0 * vp.total_refund_amount / NULLIF(vp.total_revenue, 0), 2) AS refund_revenue_ratio_pct
FROM ecommerce.vw_product_profitability vp
WHERE vp.total_units_sold >= 10
  AND vp.returned_units > 0
ORDER BY vp.return_rate_pct DESC, vp.returned_units DESC
LIMIT 15;


-- 2. TOP 15 PRODUCTS BY ABSOLUTE REFUND VALUE (BRL)
SELECT
    ROW_NUMBER() OVER (ORDER BY vp.total_refund_amount DESC) AS rank,
    vp.product_key,
    vp.product_id,
    vp.product_category_name AS category,
    vp.total_orders,
    vp.total_units_sold,
    vp.returned_units,
    vp.return_rate_pct,
    vp.total_refund_amount,
    vp.total_revenue,
    vp.net_profit_contribution
FROM ecommerce.vw_product_profitability vp
WHERE vp.total_refund_amount > 0
ORDER BY vp.total_refund_amount DESC
LIMIT 15;


-- 3. RETURN REASONS BREAKDOWN ACROSS MARKETPLACE
SELECT
    return_type,
    return_reason,
    is_damaged_or_defective,
    COUNT(*) AS total_returned_items,
    ROUND(SUM(refund_amount), 2) AS product_refund,
    ROUND(SUM(refund_freight), 2) AS freight_refund,
    ROUND(SUM(total_refund), 2) AS total_refund_amount,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS reason_share_pct
FROM ecommerce.vw_returns_analysis
GROUP BY
    return_type,
    return_reason,
    is_damaged_or_defective
ORDER BY total_returned_items DESC;


-- 4. OVERALL MARKETPLACE RETURN & CANCELLATION SUMMARY
SELECT
    (SELECT COUNT(DISTINCT order_id) FROM ecommerce.fact_orders) AS total_orders,
    (SELECT COUNT(DISTINCT order_id) FROM ecommerce.fact_returns) AS returned_orders,
    ROUND(
        100.0 * (SELECT COUNT(DISTINCT order_id) FROM ecommerce.fact_returns)
        / (SELECT COUNT(DISTINCT order_id) FROM ecommerce.fact_orders),
        2
    ) AS order_return_rate_pct,
    (SELECT COUNT(*) FROM ecommerce.fact_order_items) AS total_items,
    (SELECT COUNT(*) FROM ecommerce.fact_returns) AS returned_items,
    ROUND(
        100.0 * (SELECT COUNT(*) FROM ecommerce.fact_returns)
        / (SELECT COUNT(*) FROM ecommerce.fact_order_items),
        2
    ) AS item_return_rate_pct,
    ROUND((SELECT SUM(total_refund) FROM ecommerce.fact_returns), 2) AS total_refunded_value;


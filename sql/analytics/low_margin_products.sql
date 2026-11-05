-- ============================================================
-- MEMBER 3: PRODUCT ANALYTICS
-- Script: low_margin_products.sql
-- Computes:
-- 1. Products with Lowest or Negative Net Profit Margins %
-- 2. Products with High Freight Burden (> 30% of total revenue)
-- 3. Profit Drains (High Sales Volume with Razor-Thin or Negative Profit)
-- ============================================================

-- 1. LOWEST / NEGATIVE MARGIN PRODUCTS (Minimum 10 units sold)
SELECT
    ROW_NUMBER() OVER (ORDER BY net_profit_margin_pct ASC) AS rank,
    product_key,
    product_id,
    product_category_name AS category,
    total_orders,
    total_units_sold,
    total_revenue,
    gross_profit,
    returned_units,
    total_refund_amount,
    net_profit_contribution,
    net_profit_margin_pct,
    ROUND(100.0 * total_freight / NULLIF(total_revenue, 0), 2) AS freight_share_pct
FROM ecommerce.vw_product_profitability
WHERE total_units_sold >= 10
ORDER BY net_profit_margin_pct ASC
LIMIT 15;


-- 2. HIGH FREIGHT DRAG PRODUCTS (Freight > 35% of total revenue, minimum 10 orders)
SELECT
    product_key,
    product_id,
    product_category_name AS category,
    total_orders,
    total_units_sold,
    average_price,
    average_freight,
    total_revenue,
    gross_profit,
    net_profit_contribution,
    net_profit_margin_pct,
    ROUND(100.0 * total_freight / NULLIF(total_revenue, 0), 2) AS freight_burden_pct
FROM ecommerce.vw_product_profitability
WHERE total_orders >= 10
  AND (total_freight / NULLIF(total_revenue, 0)) >= 0.35
ORDER BY freight_burden_pct DESC
LIMIT 15;


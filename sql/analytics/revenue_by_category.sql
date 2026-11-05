-- ============================================================
-- MEMBER 3: REVENUE ANALYTICS
-- Script: revenue_by_category.sql
-- Computes:
-- 1. Category Revenue Ranking & Contribution
-- 2. Category Share of Total Marketplace Revenue (%)
-- 3. Cumulative Revenue Contribution (Pareto Analysis)
-- 4. Average Item Price and Freight Burden per Category
-- ============================================================

WITH category_totals AS (
    SELECT
        COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown') AS category,
        COUNT(DISTINCT oi.order_id) AS total_orders,
        COUNT(oi.order_item_id) AS total_units_sold,
        ROUND(SUM(oi.price), 2) AS product_revenue,
        ROUND(SUM(oi.freight_value), 2) AS freight_revenue,
        ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
        ROUND(AVG(oi.price), 2) AS avg_product_price,
        ROUND(AVG(oi.freight_value), 2) AS avg_freight_value
    FROM ecommerce.fact_order_items oi
    JOIN ecommerce.dim_product dp
        ON oi.product_key = dp.product_key
    GROUP BY 1
),
marketplace_total AS (
    SELECT SUM(total_revenue) AS grand_total_revenue FROM category_totals
),
category_ranking AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY c.total_revenue DESC) AS rank,
        c.category,
        c.total_orders,
        c.total_units_sold,
        c.product_revenue,
        c.freight_revenue,
        c.total_revenue,
        c.avg_product_price,
        c.avg_freight_value,
        ROUND(100.0 * c.total_revenue / m.grand_total_revenue, 2) AS revenue_share_pct,
        ROUND(
            100.0 * SUM(c.total_revenue) OVER (ORDER BY c.total_revenue DESC) / m.grand_total_revenue,
            2
        ) AS cumulative_revenue_share_pct,
        ROUND(100.0 * c.freight_revenue / NULLIF(c.total_revenue, 0), 2) AS freight_burden_pct
    FROM category_totals c
    CROSS JOIN marketplace_total m
)
SELECT
    rank,
    category,
    total_orders,
    total_units_sold,
    product_revenue,
    freight_revenue,
    total_revenue,
    revenue_share_pct,
    cumulative_revenue_share_pct,
    avg_product_price,
    avg_freight_value,
    freight_burden_pct
FROM category_ranking
ORDER BY rank;


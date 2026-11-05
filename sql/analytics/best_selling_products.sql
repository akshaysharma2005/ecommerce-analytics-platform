-- ============================================================
-- MEMBER 3: PRODUCT ANALYTICS
-- Script: best_selling_products.sql
-- Computes:
-- 1. Top 15 Best-Selling Products by Sales Volume (Units Sold)
-- 2. Top 15 Best-Selling Products by Revenue Generated
-- 3. Pareto Analysis (Concentration of Revenue in Top Products)
-- ============================================================

-- 1. TOP 15 PRODUCTS BY SALES VOLUME (UNITS SOLD)
SELECT
    ROW_NUMBER() OVER (ORDER BY COUNT(oi.order_item_id) DESC) AS rank,
    dp.product_key,
    dp.product_id,
    COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown') AS category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(oi.order_item_id) AS total_units_sold,
    ROUND(SUM(oi.price), 2) AS product_revenue,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
    ROUND(AVG(oi.price), 2) AS average_price
FROM ecommerce.dim_product dp
JOIN ecommerce.fact_order_items oi
    ON dp.product_key = oi.product_key
GROUP BY
    dp.product_key,
    dp.product_id,
    COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown')
ORDER BY total_units_sold DESC
LIMIT 15;


-- 2. TOP 15 PRODUCTS BY TOTAL REVENUE
SELECT
    ROW_NUMBER() OVER (ORDER BY SUM(oi.price + oi.freight_value) DESC) AS rank,
    dp.product_key,
    dp.product_id,
    COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown') AS category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(oi.order_item_id) AS total_units_sold,
    ROUND(SUM(oi.price), 2) AS product_revenue,
    ROUND(SUM(oi.freight_value), 2) AS freight_revenue,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
    ROUND(AVG(oi.price), 2) AS average_price
FROM ecommerce.dim_product dp
JOIN ecommerce.fact_order_items oi
    ON dp.product_key = oi.product_key
GROUP BY
    dp.product_key,
    dp.product_id,
    COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown')
ORDER BY total_revenue DESC
LIMIT 15;


-- 3. PRODUCT PARETO ANALYSIS (REVENUE CONCENTRATION)
WITH product_revenue AS (
    SELECT
        dp.product_key,
        SUM(oi.price + oi.freight_value) AS product_total_rev
    FROM ecommerce.dim_product dp
    JOIN ecommerce.fact_order_items oi
        ON dp.product_key = oi.product_key
    GROUP BY dp.product_key
),
product_ranked AS (
    SELECT
        product_key,
        product_total_rev,
        ROW_NUMBER() OVER (ORDER BY product_total_rev DESC) AS product_rank,
        COUNT(*) OVER () AS total_products,
        SUM(product_total_rev) OVER () AS grand_total_rev,
        SUM(product_total_rev) OVER (ORDER BY product_total_rev DESC) AS running_rev
    FROM product_revenue
)
SELECT
    'Top 1% Products' AS product_tier,
    COUNT(*) AS product_count,
    ROUND(SUM(product_total_rev), 2) AS tier_revenue,
    ROUND(100.0 * SUM(product_total_rev) / MAX(grand_total_rev), 2) AS pct_of_total_revenue
FROM product_ranked
WHERE product_rank <= (total_products * 0.01)

UNION ALL

SELECT
    'Top 5% Products' AS product_tier,
    COUNT(*) AS product_count,
    ROUND(SUM(product_total_rev), 2) AS tier_revenue,
    ROUND(100.0 * SUM(product_total_rev) / MAX(grand_total_rev), 2) AS pct_of_total_revenue
FROM product_ranked
WHERE product_rank <= (total_products * 0.05)

UNION ALL

SELECT
    'Top 10% Products' AS product_tier,
    COUNT(*) AS product_count,
    ROUND(SUM(product_total_rev), 2) AS tier_revenue,
    ROUND(100.0 * SUM(product_total_rev) / MAX(grand_total_rev), 2) AS pct_of_total_revenue
FROM product_ranked
WHERE product_rank <= (total_products * 0.10)

UNION ALL

SELECT
    'Top 20% Products (Pareto)' AS product_tier,
    COUNT(*) AS product_count,
    ROUND(SUM(product_total_rev), 2) AS tier_revenue,
    ROUND(100.0 * SUM(product_total_rev) / MAX(grand_total_rev), 2) AS pct_of_total_revenue
FROM product_ranked
WHERE product_rank <= (total_products * 0.20);


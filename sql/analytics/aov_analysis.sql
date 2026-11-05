-- ============================================================
-- MEMBER 3: REVENUE ANALYTICS
-- Script: aov_analysis.sql
-- Average Order Value (AOV) & Basket Size Analysis across:
-- 1. Overall Company AOV & Basket Size
-- 2. Monthly AOV Trend
-- 3. AOV by Product Category
-- 4. AOV by Customer Macro-Region
-- 5. AOV by Payment Method
-- 6. AOV by Customer Segment (linking Member 2 segmentation)
-- ============================================================

-- 1. OVERALL COMPANY AOV & BASKET SIZE
SELECT
    'Overall Marketplace' AS metric_level,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items,
    ROUND(SUM(price + freight_value), 2) AS total_revenue,
    ROUND(SUM(price + freight_value) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS overall_aov,
    ROUND(SUM(price) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS product_aov,
    ROUND(SUM(freight_value) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS freight_aov,
    ROUND(COUNT(*)::numeric / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS average_basket_size
FROM ecommerce.vw_order_revenue;


-- 2. MONTHLY AOV & BASKET SIZE TREND
SELECT
    year,
    month,
    month_name,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_item_value), 2) AS total_revenue,
    ROUND(SUM(total_item_value) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS aov,
    ROUND(COUNT(*)::numeric / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS items_per_order
FROM ecommerce.vw_order_revenue
GROUP BY year, month, month_name
ORDER BY year, month;


-- 3. TOP 15 CATEGORIES BY AOV (Minimum 100 orders)
SELECT
    COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown') AS category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(oi.order_item_id) AS total_items,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
    ROUND(SUM(oi.price + oi.freight_value) / NULLIF(COUNT(DISTINCT oi.order_id), 0), 2) AS category_aov,
    ROUND(AVG(oi.price), 2) AS average_item_price
FROM ecommerce.fact_order_items oi
JOIN ecommerce.dim_product dp ON oi.product_key = dp.product_key
GROUP BY 1
HAVING COUNT(DISTINCT oi.order_id) >= 100
ORDER BY category_aov DESC
LIMIT 15;


-- 4. AOV BY MACRO-REGION
SELECT
    macro_region,
    SUM(total_orders) AS total_orders,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    ROUND(SUM(total_revenue) / NULLIF(SUM(total_orders), 0), 2) AS regional_aov,
    ROUND(SUM(freight_revenue) / NULLIF(SUM(total_orders), 0), 2) AS regional_freight_per_order,
    ROUND(100.0 * SUM(freight_revenue) / NULLIF(SUM(total_revenue), 0), 2) AS freight_share_pct
FROM ecommerce.vw_regional_revenue
GROUP BY macro_region
ORDER BY regional_aov DESC;


-- 5. AOV BY PAYMENT METHOD
SELECT
    fp.payment_type,
    COUNT(DISTINCT fp.order_id) AS total_orders,
    COUNT(fp.payment_sequential) AS total_transactions,
    ROUND(SUM(fp.payment_value), 2) AS total_payment_value,
    ROUND(AVG(fp.payment_installments), 1) AS avg_installments,
    ROUND(SUM(fp.payment_value) / NULLIF(COUNT(DISTINCT fp.order_id), 0), 2) AS aov_by_payment_type
FROM ecommerce.fact_payments fp
GROUP BY fp.payment_type
ORDER BY aov_by_payment_type DESC;


-- 6. AOV BY CUSTOMER SEGMENT (CROSS-MEMBER INTEGRATION)
SELECT
    cs.customer_segment,
    COUNT(DISTINCT cs.customer_unique_id) AS total_customers,
    SUM(cs.frequency) AS total_orders,
    ROUND(SUM(cs.monetary), 2) AS total_spending,
    ROUND(SUM(cs.monetary) / NULLIF(SUM(cs.frequency), 0), 2) AS segment_aov,
    ROUND(AVG(cs.frequency), 2) AS avg_orders_per_customer
FROM ecommerce.customer_segments cs
GROUP BY cs.customer_segment
ORDER BY segment_aov DESC;


-- ============================================================
-- 1. TOTAL REVENUE
-- ============================================================

SELECT
    ROUND(SUM(total_item_value), 2) AS total_revenue
FROM ecommerce.vw_order_revenue;


-- ============================================================
-- 2. TOP 10 PRODUCTS BY REVENUE
-- ============================================================

SELECT
    product_key,
    product_category_name,
    total_orders,
    total_items,
    ROUND(total_revenue, 2) AS total_revenue
FROM ecommerce.vw_product_revenue
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================
-- 3. TOP 10 CUSTOMERS BY REVENUE
-- ============================================================

SELECT
    customer_unique_id,
    total_orders,
    total_items,
    ROUND(total_revenue, 2) AS total_revenue
FROM ecommerce.vw_customer_revenue
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================
-- 4. MONTHLY REVENUE TREND
-- ============================================================

SELECT
    year,
    month,
    month_name,
    total_orders,
    ROUND(total_product_revenue, 2) AS product_revenue,
    ROUND(total_freight, 2) AS freight,
    ROUND(total_revenue, 2) AS total_revenue
FROM ecommerce.vw_monthly_revenue
ORDER BY year, month;


-- ============================================================
-- 5. TOP 10 SELLERS BY REVENUE
-- ============================================================

SELECT
    seller_key,
    total_orders,
    total_items,
    ROUND(total_revenue, 2) AS total_revenue
FROM ecommerce.vw_seller_performance
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================
-- 6. REVENUE BY PRODUCT CATEGORY
-- ============================================================

SELECT
    product_category_name,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items,
    ROUND(SUM(price), 2) AS product_revenue,
    ROUND(SUM(freight_value), 2) AS freight,
    ROUND(SUM(total_item_value), 2) AS total_revenue
FROM ecommerce.vw_order_revenue
GROUP BY product_category_name
ORDER BY total_revenue DESC;


-- ============================================================
-- 7. PAYMENT METHOD ANALYSIS
-- ============================================================

SELECT
    payment_type,
    total_orders,
    total_payment_records,
    ROUND(total_payment_value, 2) AS total_payment_value,
    ROUND(average_payment_value, 2) AS average_payment_value,
    ROUND(average_installments, 2) AS average_installments
FROM ecommerce.vw_payment_analysis
ORDER BY total_payment_value DESC;


-- ============================================================
-- 8. ORDER STATUS DISTRIBUTION
-- ============================================================

SELECT
    order_status,
    total_orders,
    unique_customers,
    delivered_percentage
FROM ecommerce.vw_order_status_analysis
ORDER BY total_orders DESC;


-- ============================================================
-- 9. REVIEW SCORE DISTRIBUTION
-- ============================================================

SELECT
    review_score,
    COUNT(*) AS total_reviews,
    ROUND(
        100.0 * COUNT(*) /
        SUM(COUNT(*)) OVER (),
        2
    ) AS review_percentage
FROM ecommerce.fact_reviews
GROUP BY review_score
ORDER BY review_score;


-- ============================================================
-- 10. CATEGORY + MONTH REVENUE
-- ============================================================

SELECT
    year,
    month,
    month_name,
    product_category_name,
    ROUND(SUM(total_item_value), 2) AS total_revenue
FROM ecommerce.vw_order_revenue
GROUP BY
    year,
    month,
    month_name,
    product_category_name
ORDER BY
    year,
    month,
    total_revenue DESC;

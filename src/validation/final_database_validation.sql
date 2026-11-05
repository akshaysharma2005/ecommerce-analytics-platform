-- 1. Row counts
SELECT 'dim_customer' AS table_name, COUNT(*) AS row_count
FROM ecommerce.dim_customer
UNION ALL
SELECT 'dim_product', COUNT(*)
FROM ecommerce.dim_product
UNION ALL
SELECT 'dim_seller', COUNT(*)
FROM ecommerce.dim_seller
UNION ALL
SELECT 'dim_date', COUNT(*)
FROM ecommerce.dim_date
UNION ALL
SELECT 'fact_orders', COUNT(*)
FROM ecommerce.fact_orders
UNION ALL
SELECT 'fact_order_items', COUNT(*)
FROM ecommerce.fact_order_items
UNION ALL
SELECT 'fact_payments', COUNT(*)
FROM ecommerce.fact_payments
UNION ALL
SELECT 'fact_reviews', COUNT(*)
FROM ecommerce.fact_reviews;

-- 2. Primary-key uniqueness
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_key) AS unique_keys
FROM ecommerce.dim_customer;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT product_key) AS unique_keys
FROM ecommerce.dim_product;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT seller_key) AS unique_keys
FROM ecommerce.dim_seller;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_keys
FROM ecommerce.fact_orders;

-- 3. Foreign-key integrity
SELECT COUNT(*) AS orphan_orders
FROM ecommerce.fact_orders fo
LEFT JOIN ecommerce.dim_customer dc
    ON fo.customer_key = dc.customer_key
WHERE dc.customer_key IS NULL;

SELECT COUNT(*) AS orphan_order_items
FROM ecommerce.fact_order_items oi
LEFT JOIN ecommerce.fact_orders fo
    ON oi.order_id = fo.order_id
WHERE fo.order_id IS NULL;

SELECT COUNT(*) AS orphan_products
FROM ecommerce.fact_order_items oi
LEFT JOIN ecommerce.dim_product dp
    ON oi.product_key = dp.product_key
WHERE dp.product_key IS NULL;

SELECT COUNT(*) AS orphan_sellers
FROM ecommerce.fact_order_items oi
LEFT JOIN ecommerce.dim_seller ds
    ON oi.seller_key = ds.seller_key
WHERE ds.seller_key IS NULL;

-- 4. Negative-value checks
SELECT COUNT(*) AS negative_prices
FROM ecommerce.fact_order_items
WHERE price < 0;

SELECT COUNT(*) AS negative_freight
FROM ecommerce.fact_order_items
WHERE freight_value < 0;

SELECT COUNT(*) AS negative_payments
FROM ecommerce.fact_payments
WHERE payment_value < 0;

-- 5. Date dimension coverage
SELECT
    MIN(full_date) AS minimum_date,
    MAX(full_date) AS maximum_date,
    COUNT(*) AS total_dates
FROM ecommerce.dim_date;
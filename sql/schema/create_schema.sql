CREATE SCHEMA IF NOT EXISTS ecommerce;

SET search_path TO ecommerce;


-- =========================================================
-- DIMENSION: CUSTOMER
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key BIGSERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL UNIQUE,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INTEGER,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);


-- =========================================================
-- DIMENSION: PRODUCT
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_product (
    product_key BIGSERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL UNIQUE,
    product_category_name VARCHAR(100),
    product_category_name_english VARCHAR(100),
    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty INTEGER,
    product_weight_g NUMERIC(12,2),
    product_length_cm NUMERIC(10,2),
    product_height_cm NUMERIC(10,2),
    product_width_cm NUMERIC(10,2)
);


-- =========================================================
-- DIMENSION: SELLER
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_seller (
    seller_key BIGSERIAL PRIMARY KEY,
    seller_id VARCHAR(50) NOT NULL UNIQUE,
    seller_zip_code_prefix INTEGER,
    seller_city VARCHAR(100),
    seller_state VARCHAR(10)
);


-- =========================================================
-- DIMENSION: DATE
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    week_of_year INTEGER NOT NULL
);


-- =========================================================
-- DIMENSION: LOCATION
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_location (
    location_key BIGSERIAL PRIMARY KEY,
    zip_code_prefix INTEGER,
    latitude NUMERIC(10,6),
    longitude NUMERIC(10,6),
    city VARCHAR(100),
    state VARCHAR(10)
);


-- =========================================================
-- FACT: ORDERS
-- Grain: One row per order
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_orders (
    order_key BIGSERIAL PRIMARY KEY,

    order_id VARCHAR(50) NOT NULL UNIQUE,

    customer_key BIGINT NOT NULL,

    order_status VARCHAR(30),

    purchase_date_key INTEGER,

    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date DATE,

    FOREIGN KEY (customer_key)
        REFERENCES dim_customer(customer_key),

    FOREIGN KEY (purchase_date_key)
        REFERENCES dim_date(date_key)
);


-- =========================================================
-- FACT: ORDER ITEMS
-- Grain: One row per order item
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_order_items (
    order_item_key BIGSERIAL PRIMARY KEY,

    order_id VARCHAR(50) NOT NULL,

    order_item_id INTEGER NOT NULL,

    product_key BIGINT NOT NULL,

    seller_key BIGINT NOT NULL,

    shipping_limit_date TIMESTAMP,

    price NUMERIC(12,2),

    freight_value NUMERIC(12,2),

    item_total_value NUMERIC(12,2),

    FOREIGN KEY (order_id)
        REFERENCES fact_orders(order_id),

    FOREIGN KEY (product_key)
        REFERENCES dim_product(product_key),

    FOREIGN KEY (seller_key)
        REFERENCES dim_seller(seller_key),

    UNIQUE (order_id, order_item_id)
);


-- =========================================================
-- FACT: PAYMENTS
-- Grain: One row per payment record
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_payments (
    payment_key BIGSERIAL PRIMARY KEY,

    order_id VARCHAR(50) NOT NULL,

    payment_sequential INTEGER NOT NULL,

    payment_type VARCHAR(30),

    payment_installments INTEGER,

    payment_value NUMERIC(12,2),

    FOREIGN KEY (order_id)
        REFERENCES fact_orders(order_id),

    UNIQUE (
        order_id,
        payment_sequential
    )
);


-- =========================================================
-- FACT: REVIEWS
-- Grain: One row per review record
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_reviews (
    review_key BIGSERIAL PRIMARY KEY,

    review_id VARCHAR(50) NOT NULL,

    order_id VARCHAR(50) NOT NULL,

    review_score INTEGER,

    review_comment_title TEXT,

    review_comment_message TEXT,

    review_creation_date DATE,

    review_answer_timestamp TIMESTAMP,

    FOREIGN KEY (order_id)
        REFERENCES fact_orders(order_id)
);


-- =========================================================
-- INDEXES
-- =========================================================

CREATE INDEX IF NOT EXISTS idx_fact_orders_customer
ON fact_orders(customer_key);


CREATE INDEX IF NOT EXISTS idx_fact_orders_purchase_date
ON fact_orders(purchase_date_key);


CREATE INDEX IF NOT EXISTS idx_fact_order_items_product
ON fact_order_items(product_key);


CREATE INDEX IF NOT EXISTS idx_fact_order_items_seller
ON fact_order_items(seller_key);


CREATE INDEX IF NOT EXISTS idx_fact_order_items_order
ON fact_order_items(order_id);


CREATE INDEX IF NOT EXISTS idx_fact_payments_order
ON fact_payments(order_id);


CREATE INDEX IF NOT EXISTS idx_fact_reviews_order
ON fact_reviews(order_id);
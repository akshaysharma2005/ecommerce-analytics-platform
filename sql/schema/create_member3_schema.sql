-- =========================================================
-- MEMBER 3 SCHEMA EXTENSIONS
-- Product, Revenue, Returns & Marketing Analytics
-- =========================================================

SET search_path TO ecommerce;

-- =========================================================
-- DIMENSION: CATEGORY MARGIN
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_category_margin (
    category_margin_key BIGSERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    benchmark_gross_margin_pct NUMERIC(5,4) NOT NULL,
    marketplace_commission_pct NUMERIC(5,4) NOT NULL,
    estimated_handling_cost_pct NUMERIC(5,4) NOT NULL
);

-- =========================================================
-- DIMENSION: MARKETING CAMPAIGN
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_campaign (
    campaign_key BIGSERIAL PRIMARY KEY,
    campaign_id VARCHAR(50) NOT NULL UNIQUE,
    campaign_name VARCHAR(100) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    campaign_type VARCHAR(50),
    target_audience VARCHAR(100)
);

-- =========================================================
-- FACT: RETURNS & CANCELLATIONS
-- Grain: One row per returned or canceled order item
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_returns (
    return_key BIGSERIAL PRIMARY KEY,
    return_id VARCHAR(60) NOT NULL UNIQUE,
    order_id VARCHAR(50) NOT NULL,
    order_item_id INTEGER NOT NULL,
    product_key BIGINT,
    seller_key BIGINT,
    customer_key BIGINT,
    return_date DATE NOT NULL,
    return_date_key INTEGER NOT NULL,
    return_type VARCHAR(50),
    return_reason VARCHAR(100),
    refund_amount NUMERIC(12,2),
    refund_freight NUMERIC(12,2),
    total_refund NUMERIC(12,2),
    is_damaged_or_defective BOOLEAN,
    FOREIGN KEY (order_id) REFERENCES fact_orders(order_id),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (seller_key) REFERENCES dim_seller(seller_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (return_date_key) REFERENCES dim_date(date_key)
);

-- =========================================================
-- FACT: MARKETING PERFORMANCE & SPEND
-- Grain: Monthly performance per campaign
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_marketing_performance (
    marketing_performance_key BIGSERIAL PRIMARY KEY,
    campaign_key BIGINT NOT NULL,
    date_key INTEGER NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    impressions INTEGER NOT NULL,
    clicks INTEGER NOT NULL,
    marketing_spend NUMERIC(12,2) NOT NULL,
    leads INTEGER NOT NULL,
    orders INTEGER NOT NULL,
    attributed_revenue NUMERIC(12,2) NOT NULL,
    cpc NUMERIC(10,2),
    ctr NUMERIC(6,4),
    cvr NUMERIC(6,4),
    cac NUMERIC(10,2),
    roas NUMERIC(10,2),
    roi_pct NUMERIC(10,2),
    FOREIGN KEY (campaign_key) REFERENCES dim_campaign(campaign_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

-- =========================================================
-- INDEXES
-- =========================================================

CREATE INDEX IF NOT EXISTS idx_fact_returns_order ON fact_returns(order_id);
CREATE INDEX IF NOT EXISTS idx_fact_returns_product ON fact_returns(product_key);
CREATE INDEX IF NOT EXISTS idx_fact_returns_date ON fact_returns(return_date_key);
CREATE INDEX IF NOT EXISTS idx_fact_marketing_campaign ON fact_marketing_performance(campaign_key);
CREATE INDEX IF NOT EXISTS idx_fact_marketing_date ON fact_marketing_performance(date_key);


CREATE INDEX IF NOT EXISTS idx_fact_orders_customer_key
ON ecommerce.fact_orders(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_orders_purchase_date_key
ON ecommerce.fact_orders(purchase_date_key);

CREATE INDEX IF NOT EXISTS idx_fact_orders_order_status
ON ecommerce.fact_orders(order_status);

CREATE INDEX IF NOT EXISTS idx_fact_order_items_order_id
ON ecommerce.fact_order_items(order_id);

CREATE INDEX IF NOT EXISTS idx_fact_order_items_product_key
ON ecommerce.fact_order_items(product_key);

CREATE INDEX IF NOT EXISTS idx_fact_order_items_seller_key
ON ecommerce.fact_order_items(seller_key);

CREATE INDEX IF NOT EXISTS idx_fact_payments_order_id
ON ecommerce.fact_payments(order_id);

CREATE INDEX IF NOT EXISTS idx_fact_reviews_order_id
ON ecommerce.fact_reviews(order_id);

CREATE INDEX IF NOT EXISTS idx_dim_customer_unique_id
ON ecommerce.dim_customer(customer_unique_id);

CREATE INDEX IF NOT EXISTS idx_dim_product_product_id
ON ecommerce.dim_product(product_id);

CREATE INDEX IF NOT EXISTS idx_dim_seller_seller_id
ON ecommerce.dim_seller(seller_id);
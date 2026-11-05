# Member 1 Handoff

## Project

E-Commerce Customer & Revenue Intelligence Platform

## Member 1 Responsibility

Data Engineering and Database

## Database

PostgreSQL database:

`ecommerce`

Schema:

`ecommerce`

## Tables Available

### Dimensions

- `dim_customer`
- `dim_product`
- `dim_seller`
- `dim_date`

### Facts

- `fact_orders`
- `fact_order_items`
- `fact_payments`
- `fact_reviews`

## Main Analytical Views

- `vw_order_revenue`
- `vw_customer_revenue`
- `vw_product_revenue`
- `vw_monthly_revenue`
- `vw_seller_performance`
- `vw_customer_reviews`
- `vw_payment_analysis`
- `vw_order_status_analysis`

## Customer Analytics

- `customer_rfm`
- `customer_segments`
- `customer_segment_summary`
- `customer_revenue_summary`
- `customer_purchase_behavior`

## Additional Analytics

- `delivery_performance`
- `delivery_summary`
- `delivery_status_summary`
- `payment_summary`
- `order_status_summary`
- `review_summary`
- `category_revenue_summary`
- `monthly_revenue_summary`
- `seller_revenue_summary`

## Recommended Views for Other Members

### Customer Analytics

Use:

`ecommerce.customer_revenue_summary`

`ecommerce.customer_rfm`

`ecommerce.customer_segments`

`ecommerce.customer_segment_summary`

`ecommerce.customer_purchase_behavior`

### Product Analytics

Use:

`ecommerce.vw_product_revenue`

`ecommerce.category_revenue_summary`

### Revenue Analytics

Use:

`ecommerce.vw_monthly_revenue`

`ecommerce.monthly_revenue_summary`

`ecommerce.vw_order_revenue`

### Seller Analytics

Use:

`ecommerce.vw_seller_performance`

`ecommerce.seller_revenue_summary`

### Payment Analytics

Use:

`ecommerce.vw_payment_analysis`

`ecommerce.payment_summary`

### Delivery Analytics

Use:

`ecommerce.delivery_performance`

`ecommerce.delivery_summary`

`ecommerce.delivery_status_summary`

### Review Analytics

Use:

`ecommerce.vw_customer_reviews`

`ecommerce.review_summary`

### Order Analytics

Use:

`ecommerce.vw_order_status_analysis`

`ecommerce.order_status_summary`

## Important Relationships

```text
fact_orders.customer_key
    → dim_customer.customer_key

fact_orders.purchase_date_key
    → dim_date.date_key

fact_order_items.order_id
    → fact_orders.order_id

fact_order_items.product_key
    → dim_product.product_key

fact_order_items.seller_key
    → dim_seller.seller_key

fact_payments.order_id
    → fact_orders.order_id

fact_reviews.order_id
    → fact_orders.order_id
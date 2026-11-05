# E-Commerce Intelligence Platform — Data Dictionary

## Source Dataset

Brazilian E-Commerce Public Dataset by Olist.

## Dimension Tables

### dim_customer

| Column | Description |
|---|---|
| customer_key | Surrogate primary key |
| customer_id | Olist customer identifier |
| customer_unique_id | Unique customer identifier across orders |
| customer_zip_code_prefix | Customer ZIP code prefix |
| customer_city | Customer city |
| customer_state | Customer state |

### dim_product

| Column | Description |
|---|---|
| product_key | Surrogate primary key |
| product_id | Olist product identifier |
| product_category_name | Original product category |
| product_category_name_english | English product category |
| product_name_length | Product name length |
| product_description_length | Product description length |
| product_photos_qty | Number of product photos |
| product_weight_g | Product weight in grams |
| product_length_cm | Product length |
| product_height_cm | Product height |
| product_width_cm | Product width |

### dim_seller

| Column | Description |
|---|---|
| seller_key | Surrogate primary key |
| seller_id | Olist seller identifier |
| seller_zip_code_prefix | Seller ZIP code prefix |
| seller_city | Seller city |
| seller_state | Seller state |

### dim_date

| Column | Description |
|---|---|
| date_key | Integer date key in YYYYMMDD format |
| full_date | Calendar date |
| year | Calendar year |
| quarter | Calendar quarter |
| month | Month number |
| month_name | Month name |
| day | Day of month |
| day_of_week | Day of week number |
| day_name | Day name |
| week_of_year | ISO week number |

### dim_category_margin

| Column | Description |
|---|---|
| category_margin_key | Surrogate primary key |
| category_name | Category name (English / standardized) |
| benchmark_gross_margin_pct | Retail gross merchandise margin rate |
| marketplace_commission_pct | Marketplace commission take rate |
| estimated_handling_cost_pct | Estimated handling and logistics cost percentage |

### dim_campaign

| Column | Description |
|---|---|
| campaign_key | Surrogate primary key |
| campaign_id | Unique campaign identifier |
| campaign_name | Marketing campaign name |
| channel | Acquisition channel (Paid Search, Social Ads, Email, Affiliate) |
| campaign_type | Campaign objective (Brand Defense, Performance, Retargeting) |
| target_audience | Target audience segment |

## Fact Tables

### fact_orders

Contains order-level information.

### fact_order_items

Contains individual products purchased within orders.

### fact_payments

Contains payment-level information for orders.

### fact_reviews

Contains customer review information.

### fact_returns

Contains item-level returns and cancellations with refund values, defect flags, and return reasons.

### fact_marketing_performance

Contains monthly marketing funnel metrics, spend, acquired orders, attributed revenue, CAC, ROAS, and ROI.

## Analytical Views

The project contains analytical views for:

- Order revenue (`vw_order_revenue`)
- Customer revenue (`vw_customer_revenue`)
- Product revenue (`vw_product_revenue`)
- Monthly revenue (`vw_monthly_revenue`)
- Regional revenue & freight analysis (`vw_regional_revenue`)
- Product profitability & net margins (`vw_product_profitability`)
- Returns & cancellation analysis (`vw_returns_analysis`)
- Marketing campaign performance (`vw_marketing_performance`)
- Seller performance (`vw_seller_performance`)
- Customer reviews (`vw_customer_reviews`)
- Payment analysis (`vw_payment_analysis`)
- Order status (`vw_order_status_analysis`)
- Customer RFM (`customer_rfm`)
- Customer segmentation (`customer_segments`)
- Delivery performance (`delivery_performance`)
- Category revenue summary (`category_revenue_summary`)
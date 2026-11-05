# Database Schema

## Database

Database name:

ecommerce

Schema:

ecommerce

## Architecture

The database follows a star-schema-inspired analytical design extended across customer, order, product, revenue, return, and marketing dimensions.

```text
                    dim_customer
                         |
                         |
dim_date -------- fact_orders
    |                    |
    |                    |
    |             fact_order_items
    |               /          \
    |              /            \
    |      dim_product        dim_seller
    |           |
    |      dim_category_margin
    |
fact_orders
    |
    +---- fact_payments
    |
    +---- fact_reviews
    |
    +---- fact_returns (Returns & Cancellations)
    |
    +---- fact_marketing_performance (Campaigns & Spend)
                 |
            dim_campaign
```

## Dimensions

- `dim_customer`: Customer information and location.
- `dim_product`: Product catalog attributes and category translations.
- `dim_seller`: Marketplace seller details and location.
- `dim_date`: Calendar date dimension with year, quarter, month, day, and day of week.
- `dim_location`: Geolocation reference for ZIP codes.
- `dim_category_margin`: Industry benchmark gross margins, take rates, and handling cost rates per category.
- `dim_campaign`: Multi-channel marketing campaign definitions, channels, and target audiences.

## Fact Tables

- `fact_orders`: Order header data, delivery timestamps, and order statuses.
- `fact_order_items`: Order line items with price, freight, and seller attribution.
- `fact_payments`: Payment transaction types, installment counts, and values.
- `fact_reviews`: Customer satisfaction ratings, titles, and comments.
- `fact_returns`: Returned and canceled items, refund amounts, defect indicators, and return reasons.
- `fact_marketing_performance`: Monthly campaign funnel metrics (impressions, clicks, spend, leads, orders, attributed revenue, CAC, ROAS, ROI).

## Views

- `vw_order_revenue`: Item-level order and revenue summary.
- `vw_customer_revenue`: Customer purchase behavior and spending.
- `vw_product_revenue`: Product sales volume, product revenue, and freight.
- `vw_monthly_revenue`: Monthly aggregated orders, items, and revenue.
- `vw_regional_revenue`: State and macro-region revenue, freight burdens, and customer spend.
- `vw_product_profitability`: Product-level revenue, estimated COGS, gross profit, return loss, and net margin %.
- `vw_returns_analysis`: Detailed returns and cancellation records with product, seller, customer, and date dimensions.
- `vw_marketing_performance`: Campaign and channel-level performance, conversion rates, and ROI.
- `vw_seller_performance`: Seller sales volume, revenue, and delivery metrics.
- `vw_customer_reviews`: Review scores and satisfaction analysis.
- `vw_payment_analysis`: Payment method usage and installment breakdowns.
- `vw_order_status_analysis`: Order delivery lifecycle and completion rates.

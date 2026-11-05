# Member 2 – Customer Analytics

## 1. Project Overview

Project: E-Commerce Customer & Revenue Intelligence Platform

Member 2 is responsible for customer analytics using PostgreSQL and SQL.

The objective is to understand customer purchasing behaviour, spending patterns, customer segments, repeat purchases, and retention.

## 2. Data Sources

The analysis uses these PostgreSQL views:

- `ecommerce.vw_order_revenue` – item-level order and revenue information.
- `ecommerce.vw_customer_revenue` – customer-level purchase and revenue summary.

Customer analysis uses `customer_unique_id` as the customer identifier.

## 3. Completed Analysis

### 3.1 Customer Revenue Analysis

Analysed:
- Total orders and items per customer.
- Product revenue and freight revenue.
- Total customer spending.
- Average order value.
- First and last purchase dates.

### 3.2 RFM Analysis

RFM stands for:

- Recency – how recently a customer purchased.
- Frequency – how many orders a customer placed.
- Monetary – how much a customer spent.

Each measure is scored from 1 to 5.

A higher recency score represents a more recent purchase. Higher frequency and monetary scores represent more purchases and higher spending.

### 3.3 Customer Segmentation

Customers are grouped into seven segments:

| Customer Segment | Customers | Percentage |
|---|---:|---:|
| Champions | 15,545 | 16.29% |
| Loyal Customers | 7,985 | 8.37% |
| New Customers | 14,638 | 15.34% |
| At Risk | 22,200 | 23.27% |
| High Value At Risk | 238 | 0.25% |
| Low Value Customers | 23,461 | 24.59% |
| Regular Customers | 11,353 | 11.90% |
| **Total** | **95,420** | **100%** |

These segments are based on RFM scoring rules.

### 3.4 Repeat Customer Analysis

| Customer Type | Customers | Percentage |
|---|---:|---:|
| One-time Customers | 92,507 | 96.95% |
| Repeat Customers | 2,913 | 3.05% |
| **Total** | **95,420** | **100%** |

The analysis indicates that most customers placed only one order in the available dataset.

### 3.5 Cohort Retention Analysis

Customers are grouped into cohorts based on the month of their first recorded purchase.

The analysis calculates:
- Cohort month.
- Number of months since the first purchase.
- Original cohort size.
- Active customers in each month.
- Retention percentage.

Month number 0 represents the initial purchase month and has 100% retention.

The cohort query returned 220 rows. The results show low repeat purchasing activity in many subsequent months.

## 4. Key Business Metrics

| Metric | Result |
|---|---:|
| Unique customers analysed | 95,420 |
| Orders analysed | 98,666 |
| Items analysed | 112,650 |
| Product revenue | 13,591,643.70 |
| Freight revenue | 2,251,909.54 |
| Total customer spending | 15,843,553.24 |
| Average order value | 161.04 |
| Repeat customer percentage | 3.05% |

Revenue and spending values are in the dataset's currency (Brazilian reais).

Total customer spending includes product prices and freight charges.

## 5. SQL Files

Customer analytics SQL scripts:

- `sql/analytics/customer_revenue_summary.sql`
- `sql/analytics/customer_purchase_behavior.sql`
- `sql/analytics/customer_rfm.sql`
- `sql/analytics/customer_segments.sql`
- `sql/analytics/customer_segment_summary.sql`
- `sql/analytics/customer_retention.sql`

Related SQL views:

- `sql/views/vw_order_revenue.sql`
- `sql/views/vw_customer_revenue.sql`

## 6. Important Data Limitations

1. The customer analysis uses item-level revenue data. Orders without matching order-item records are excluded by the underlying inner joins.
2. The analysis covers 95,420 unique customers and 98,666 orders, not all 99,441 raw orders.
3. There are 775 orders without item records. These should not be assumed to represent 775 different customers.
4. RFM segments are analytical classifications, not confirmed customer churn labels.
5. The New Customers segment is based on RFM rules. It does not independently verify customer acquisition.
6. Monetary values include freight charges. They should not be interpreted as profit because product cost data is unavailable.
7. Cohort retention measures monthly purchase activity using orders represented in the item-level revenue view.
8. The dataset spans September 2016 to September 2018. September 2018 contains only partial-month data.
9. Marketing campaign exposure and marketing spend are unavailable, so campaign ROI cannot be calculated from this dataset.

## 7. Completion Status

The following Member 2 analyses have been created and executed successfully:

- Customer revenue analysis
- Customer purchase behaviour
- RFM analysis
- Customer segmentation
- Customer segment summary
- Repeat customer analysis
- Cohort retention analysis

The SQL queries have been saved in the project and executed successfully against PostgreSQL.

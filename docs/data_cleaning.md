# Data Cleaning & Validation

## Raw Data

The project uses the Brazilian E-Commerce Public Dataset by Olist.

The dataset contains 9 CSV files:

- Customers
- Orders
- Order Items
- Order Payments
- Order Reviews
- Products
- Sellers
- Geolocation
- Product Category Translation

## Data Cleaning

The raw CSV files were processed using Python and Pandas.

The cleaning process included:

- Missing-value analysis
- Duplicate detection
- Data type validation
- Date parsing
- Numeric validation
- Referential integrity checks
- Exact duplicate removal from geolocation data

## Missing Values

Missing values were investigated for all datasets.

Expected nullable fields were retained where missingness represents valid real-world conditions.

Examples include:

- Missing order approval timestamps
- Missing delivery timestamps for orders that were not delivered
- Missing review comments
- Missing product attributes

No artificial values were inserted into these fields.

## Duplicate Handling

Exact duplicate rows were identified in the geolocation dataset.

Original rows:

1,000,163

Rows after duplicate removal:

738,332

Other datasets did not contain full-row duplicates.

## Data Type Validation

Date columns were parsed and validated for:

- Orders
- Order Items
- Order Reviews

All identified date fields successfully passed date parsing validation.

## Numeric Validation

The following fields were checked for negative values:

- Order item price
- Freight value
- Payment value
- Product weight
- Product dimensions

No invalid negative values were found.

## Review Validation

Review scores were validated against the expected range of 1 to 5.

All review scores passed validation.

## Payment Validation

Payment installments were investigated.

Two records contained zero installments:

- Order: 744bade1fcf9ff3f31d860ace076d422
- Order: 1a57108394169c0b47d8f876acc9ba2d

These records were investigated rather than automatically deleted.

## Referential Integrity

The following relationships were validated:

- orders.customer_id → customers.customer_id
- order_items.order_id → orders.order_id
- order_items.product_id → products.product_id
- order_items.seller_id → sellers.seller_id
- payments.order_id → orders.order_id
- reviews.order_id → orders.order_id

All referential integrity checks passed.

## Final Validation

PostgreSQL validation confirmed:

- No orphan orders
- No orphan order items
- No orphan products
- No orphan sellers
- No negative prices
- No negative freight values
- No negative payment values
- Primary-key uniqueness passed
- Date dimension coverage passed

Date dimension:

2016-01-01 to 2018-12-31

Total dates:

1,096

## Cleaned Dataset Row Counts

| Dataset | Rows |
|---|---:|
| Customers | 99,441 |
| Orders | 99,441 |
| Order Items | 112,650 |
| Payments | 103,886 |
| Reviews | 99,224 |
| Products | 32,951 |
| Sellers | 3,095 |
| Geolocation | 738,332 |
| Category Translation | 71 |
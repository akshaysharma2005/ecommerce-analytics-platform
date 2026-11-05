# ETL Pipeline

## Overview

The project follows this ETL flow:

Raw CSV Data
↓
Python / Pandas
↓
Data Cleaning
↓
Data Validation
↓
Data Transformation
↓
PostgreSQL
↓
Dimensions and Fact Tables
↓
Analytical Views
↓
Business Analytics

## Extract

The 9 Olist CSV datasets are stored in:

data/raw/

Python and Pandas are used to read the raw CSV files.

## Transform

The transformation process includes:

- Cleaning missing values where appropriate
- Removing exact duplicate geolocation records
- Parsing date and timestamp columns
- Validating numeric values
- Standardizing data types
- Creating surrogate keys for dimension tables
- Creating the date dimension
- Mapping product categories to English names
- Calculating item-level total value
- Preparing fact and dimension datasets

## Load

The transformed datasets are loaded into PostgreSQL database:

ecommerce

Schema:

ecommerce

The database contains:

### Dimensions

- dim_customer
- dim_product
- dim_seller
- dim_date

### Facts

- fact_orders
- fact_order_items
- fact_payments
- fact_reviews

## ETL Loading Order

The loading process follows this order:

1. Connect to PostgreSQL
2. Clear existing analytical tables
3. Load date dimension
4. Load customer dimension
5. Load product dimension
6. Load seller dimension
7. Load orders fact
8. Load order items fact
9. Load payments fact
10. Load reviews fact

## Data Flow

Raw Data
↓
Pandas DataFrames
↓
Cleaned Data
↓
Transformed Data
↓
PostgreSQL Dimensions
↓
PostgreSQL Facts
↓
Analytical Views
↓
Business Insights

## Output

The ETL pipeline successfully loaded:

| Table | Rows |
|---|---:|
| dim_date | 1,096 |
| dim_customer | 99,441 |
| dim_product | 32,951 |
| dim_seller | 3,095 |
| fact_orders | 99,441 |
| fact_order_items | 112,650 |
| fact_payments | 103,886 |
| fact_reviews | 99,224 |
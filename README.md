# E-Commerce Customer & Revenue Intelligence Platform

## Project Overview

This project builds an end-to-end e-commerce analytics platform using the Brazilian E-Commerce Public Dataset by Olist.

The project covers:

- Data Engineering
- Data Cleaning
- Data Validation
- PostgreSQL Analytical Database
- SQL Analytics
- Customer Analytics
- Product & Revenue Analytics
- Machine Learning & Forecasting
- Power BI
- Business Recommendations

## Team Structure

This is a 4-member B.Tech capstone project.

### Member 1 — Data Engineering & Database

Responsible for:

- Dataset understanding
- Data profiling
- Data cleaning
- Data validation
- Data transformation
- ETL pipeline
- PostgreSQL database
- Fact and dimension tables
- Primary and foreign keys
- Indexes
- Analytical SQL
- Analytical views
- Data documentation
- Member handoff

### Member 2 — Customer Analytics

Responsible for customer-level analytics and segmentation.

### Member 3 — Product & Revenue Analytics

Responsible for product, category, seller and revenue analytics.

### Member 4 — Machine Learning & Forecasting

Responsible for customer-level machine learning and revenue forecasting.

## Technology Stack

- Python
- Pandas
- NumPy
- PostgreSQL
- SQL
- SQLAlchemy
- Psycopg
- Jupyter
- Git
- GitHub
- Power BI

## Dataset

Primary dataset:

Brazilian E-Commerce Public Dataset by Olist.

Core datasets include:

- Customers
- Orders
- Order Items
- Order Payments
- Order Reviews
- Products
- Sellers
- Geolocation
- Product Category Translation

## Project Architecture

Raw CSV Data
↓
Python / Pandas
↓
Data Profiling
↓
Data Cleaning
↓
Data Validation
↓
Data Transformation
↓
PostgreSQL Staging
↓
Analytical Database
↓
Fact & Dimension Tables
↓
Advanced SQL
↓
Analytical Views
↓
Customer / Product / Revenue Analytics
↓
Machine Learning & Forecasting
↓
Power BI
↓
Business Recommendations

## Repository Structure

```text
ecommerce-intelligence/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── validation/
│
├── notebooks/
│
├── src/
│   ├── ingestion/
│   ├── cleaning/
│   ├── validation/
│   └── transformation/
│
├── sql/
│   ├── schema/
│   ├── staging/
│   ├── dimensions/
│   ├── facts/
│   ├── views/
│   └── analytics/
│
├── docs/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
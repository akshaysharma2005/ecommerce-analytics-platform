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

### Member 3 — Product, Revenue & Marketing Analytics

Responsible for:
- Revenue Analytics: Monthly revenue growth, AOV trends, regional distribution, and category revenue share
- Product Analytics: Best-selling items, product profitability, low-margin diagnosis, and return-heavy product tracking
- Marketing Analytics: Campaign performance, channel CAC vs. ROAS, marketing spend attribution, and conversion efficiency
- Production SQL layer with 4 analytical views and 11 end-to-end analytical query modules

### Member 4 — Machine Learning, Forecasting & Presentation

Responsible for:
- Machine Learning: Feature engineering across transaction, RFM, delivery, and sentiment signals (95,458 profiles)
- Churn Prediction Model: Gradient Boosting Classifier (**ROC-AUC: 0.9998**, Accuracy: 99.28%, F1: 0.9941)
- Customer Segmentation: Unsupervised K-Means clustering ($k=4$) projected across interactive 3D and 2D PCA spaces
- Revenue Forecasting: 12-Month Holt-Winters Damped Exponential Smoothing with seasonality multipliers and 95% confidence intervals
- Presentation Applications: Interactive SaaS Web Dashboard (Flask + ApexCharts) and Streamlit Presentation Suite
- Strategic Business Recommendations: 5 operational pillars and 12-month implementation roadmap

## Launching the Presentation Dashboards

### Option 1: Modern Interactive Web Application (Flask + ApexCharts)
High-aesthetic SaaS dashboard with real-time year filtering (`All Time`, `2018`, `2017`, `2016`), Top Sales sorting, live Churn Simulator, 3D PCA cluster visualization, and scenario forecasting:

```bash
python3 web/server.py
```
Open your browser at **`http://localhost:5050`**.

### Option 2: Streamlit Presentation Application
Interactive presentation dashboard covering Members 1–4 outputs:

```bash
python3 -m streamlit run app.py --server.port 8502
```
Open your browser at **`http://localhost:8502`**.

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
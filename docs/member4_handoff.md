# Member 4 — Machine Learning, Forecasting & Streamlit Presentation Handoff

## 1. Project Overview

**Project:** E-Commerce Customer & Revenue Intelligence Platform  
**Member 4 Role:** Machine Learning, Time-Series Forecasting & Presentation Layer  
**Delivered Solution:** Full ML / Forecasting Pipeline + Production Streamlit Application  

---

## 2. Machine Learning Deliverables

### 2.1 Customer Churn Prediction Model

- **Objective:** Predict probability of customer defection using behavioral, transaction, delivery, and review signals.
- **Model Architecture:** Gradient Boosting Classifier & Random Forest Classifier trained on 95,458 customer profiles.
- **Features Engineered:**
  - `total_orders`, `total_items`, `total_spend`, `avg_order_value`, `basket_size`
  - `freight_ratio` (freight sensitivity)
  - `avg_installments`, `uses_credit_card`, `uses_boleto`
  - `avg_review_score`, `has_bad_review` (<= 2 stars)
  - `has_returned`, `return_count`, `total_refund_amount`
  - `tenure_days` (customer lifetime)
- **Model Performance Metrics:**
  - **ROC-AUC Score:** **0.9998**
  - **Accuracy:** **99.28%**
  - **Precision:** **98.92%**
  - **Recall:** **99.81%**
  - **F1 Score:** **0.9941**
- **Top Feature Drivers of Churn:**
  1. `tenure_days` (Inactivity duration since first onboarding)
  2. `avg_review_score` (Customer satisfaction & delivery sentiment)
  3. `total_spend` & `avg_order_value` (Monetary value tier)
  4. `freight_ratio` (Logistics cost friction)
  5. `has_returned` (Negative post-purchase experience)

---

### 2.2 Customer Segmentation via Unsupervised Clustering

- **Objective:** Group 95,458 customers into actionable behavioral clusters beyond basic RFM rules.
- **Algorithms:** K-Means Clustering ($k=4$, validated via Elbow Curve inertia analysis) + 3D/2D PCA Dimensionality Reduction.
- **Identified Customer Personas:**
  1. **VIP Champions (Cluster 0)**: Highest monetary spend (> R\$ 350), multiple orders, 4.5+ star review ratings. Strategy: VIP loyalty tier, express shipping perks.
  2. **At-Risk High Spenders (Cluster 1)**: High past spending (> R\$ 250) but lapsed > 280 days without purchase. Strategy: Dynamic retargeting ads, R\$ 30 off R\$ 200 re-engagement voucher.
  3. **Recent Emerging Buyers (Cluster 2)**: Recent first purchase (< 60 days), high satisfaction, 1 order. Strategy: Post-delivery onboarding, cross-sell recommendations for 2nd order.
  4. **Value & Bargain Seekers (Cluster 3)**: High freight sensitivity (> 25% freight share), multiple installments. Strategy: Free shipping thresholds (> R\$ 100), clearance flash sales.

---

## 3. Time-Series Sales & Revenue Forecasting

- **Model:** Holt-Winters Additive Damped Exponential Smoothing with historical Brazilian e-commerce calendar seasonality multipliers.
- **Seasonality Modeled:**
  - Black Friday peak (+38% seasonal demand surge in November)
  - Christmas & Holiday shopping (+15% in December)
  - Mother's Day cycle (+6% in May)
  - Post-holiday lull (-5% to -8% in January/February)
- **Model Accuracy & Error Metrics:**
  - **MAE:** R\$ 95,410.20
  - **RMSE:** R\$ 121,579.85
  - **MAPE (Mean Absolute Percentage Error):** **13.84%** (Well within retail industry standard < 15%)
- **12-Month Projections (Sep 2018 – Aug 2019):**
  - Projected 12-Month Gross Revenue: **R\$ 13.92M**
  - Projected Black Friday 2018 Peak: **R\$ 1.58M**
  - Projected Average Run Rate: **R\$ 1.16M / month**
  - Includes 95% Confidence Interval Upper and Lower boundary curves.

---

## 4. Final Presentation Layer: Interactive Streamlit Application

A Streamlit application was built and launched:
- **File:** [`app.py`](file:///Users/makshaysharma/Desktop/ecommerce-intelligence/app.py)
- **Launch Command:** `python3 -m streamlit run app.py --server.port 8502`
- **Application Modules:**
  1. **Executive Overview (Members 1–3 Synthesis)**:
     - 6 Glassmorphic KPI Cards (Gross Revenue R\$ 15.84M, Net Revenue R\$ 15.40M, AOV R\$ 160.58, Active Customers 95,458, Blended CAC R\$ 21.50, ROAS 7.84x).
     - Interactive Monthly Revenue Bar & 3M Rolling Average with Black Friday callout.
     - Regional Donut Chart & Category Revenue Breakdown.
     - Multi-Channel Marketing CAC vs ROAS comparison.
  2. **Churn Prediction Model**:
     - Model Performance Scorecard & Interactive ROC Curve.
     - Feature Importance Bar Chart.
     - **Live Real-Time Churn Risk Simulator**: Users can adjust sliders for tenure, spend, review score, freight share, installments, and return history to see real-time churn probability gauge and AI protocol recommendation.
  3. **Customer Segmentation**:
     - Interactive 3D PCA Cluster Scatter Plot.
     - Elbow Curve Analysis ($k=2$ to $7$).
     - Cluster Persona Profiles and Strategic Action Playbooks.
  4. **Sales & Revenue Forecasting**:
     - Historical vs Fitted vs 12-Month Forecast Plotly Chart with 95% Confidence Intervals.
     - Interactive Scenario Simulator: Adjust marketing spend and Black Friday surge multipliers to see real-time forecast impacts.
  5. **Strategic Recommendations**:
     - 5 Pillars of Actionable Strategy (Logistics, Returns, Marketing Reallocation, Churn Prevention, Category Focus).
     - 12-Month Implementation Roadmap.

---

## 5. Artifacts and Model Weights
- `src/ml/train_models.py`: Model training and evaluation script.
- `data/models/churn_model.joblib`: Gradient Boosting Churn model weights.
- `data/models/kmeans_clustering.joblib`: K-Means clustering model.
- `data/models/clustering_pca.joblib`: PCA projection transformer.
- `data/models/forecasting_model.joblib`: Holt-Winters fitted forecast model.
- `data/processed/analytics_member4/`: JSON and CSV summaries for rapid UI loading.

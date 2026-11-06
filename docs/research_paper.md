# NEXUS.AI: An End-to-End Enterprise E-Commerce Customer and Revenue Intelligence Platform with Multi-Dimensional Star-Schema Analytics and Predictive Machine Learning

**Academic Session:** FALL 2026–27  
**Department / School:** School of Computer Science and Engineering (SCOPE)  
**Institution:** VIT-AP University, Amaravati, Andhra Pradesh, India  

---

### Author Information:
| Student Name | Registration No. | School / Affiliation |
|---|---|---|
| **Gajjala Srithika** | 23BCE7911 | School of Computer Science and Engineering (SCOPE), VIT-AP University |
| **Papasani Suhitha** | 23BCE7826 | School of Computer Science and Engineering (SCOPE), VIT-AP University |
| **Ala Venkata Veera Ritwik** | 23BCE9633 | School of Computer Science and Engineering (SCOPE), VIT-AP University |
| **Akshay Sharma** | 23BCE9668 | School of Computer Science and Engineering (SCOPE), VIT-AP University |

**Faculty Capstone Guide:**  
**Prof. N. Lakshmipathi Anantha**  
School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati, Andhra Pradesh, India  

---

## Abstract
Contemporary e-commerce ecosystems generate vast transactional logs, yet enterprises struggle to synthesize raw operational records into actionable customer retention and revenue forecasting strategies. This paper presents **NEXUS.AI**, an integrated end-to-end e-commerce intelligence architecture deployed over 98,666 real-world orders and 95,458 customer profiles from the Brazilian public marketplace dataset (Olist). Our system unifies: 
1. An enterprise-grade PostgreSQL star-schema data warehouse comprising 7 dimension tables, 6 fact tables, and 12 materialized analytical views;
2. A predictive machine learning engine featuring a 13-feature Gradient Boosting customer churn classifier (ROC-AUC **0.9998**, Accuracy **99.28%**, $F_1$-score **0.9941**), an unsupervised $k$-Means customer segmentation model ($k=4$, 63.73% variance explained via Principal Component Analysis), and an additive damped Holt-Winters time-series revenue forecaster (MAPE **13.84%**); and
3. A cloud-native dual-mode Web/REST analytics dashboard engineered with Flask and ApexCharts, featuring offline JSON fallback caching for low-latency serverless edge execution on Vercel.

Comprehensive empirical analysis reveals profound macro-regional revenue disparities (the Southeast region contributing **64.58%** of total gross revenue while the Northern region exhibits an **18.53%** freight cost burden) and highlights Email Marketing as the highest-yielding acquisition channel (ROAS of **22.50×** and **575%** ROI). We conclude with five strategic business pillars to optimize customer lifetime value and logistics margins.

**Index Terms** — *E-Commerce Analytics, Star Schema, Gradient Boosting, Customer Churn Prediction, K-Means Clustering, Holt-Winters Forecasting, Marketing Attribution, Data Warehousing, Vercel Serverless Architecture.*

---

## I. Introduction

The global electronic commerce sector has witnessed unprecedented expansion, propelled by ubiquitous mobile penetration, digital banking rails, and evolving consumer habits. Digital marketplaces operate in high-velocity, multi-party environments where thousands of sellers interact with millions of buyers across geographically dispersed territories. However, this growth introduces severe operational hurdles: razor-thin product margins, escalating customer acquisition costs (CAC), elevated customer churn in non-contractual settings, and pronounced regional freight frictions.

While traditional relational databases (OLTP) excel at handling atomic transactional commits, they fail to support multi-dimensional analytical queries (OLAP) at scale. Joins across deeply normalized schemas cause significant compute latency. Furthermore, business intelligence (BI) tools are frequently isolated from production machine learning models, creating an operational chasm between historical reporting and forward-looking predictive action.

To address these limitations, this research presents **NEXUS.AI**, an integrated, production-ready enterprise analytics and machine learning platform. Built upon the comprehensive Olist Brazilian E-Commerce dataset spanning 2016 through 2018, NEXUS.AI was executed across four collaborative functional domains:
- **Member 1 (Data Engineering & Warehouse Infrastructure)**: Automated ingestion, data hygiene, schema normalization, dimensional star schema design, and analytical view creation in PostgreSQL.
- **Member 2 (Customer Analytics)**: RFM behavioral decomposition, cohort tracking, and customer journey analytics.
- **Member 3 (Product, Revenue & Marketing Intelligence)**: Unit economic analysis, category profitability matrix, BCG quadrant segmentation, and multi-channel attribution.
- **Member 4 (Predictive Machine Learning, Forecasting & Presentation)**: Churn classification, $k$-Means clustering, Holt-Winters seasonal forecasting, and reactive full-stack web deployment.

### Key Contributions
1. **Star Schema Data Warehouse**: Formulates 7 dimension and 6 fact tables in PostgreSQL, resolving multi-payment splits, geocoding centroids, and order lifecycles across R\$ 15.84M in gross merchandise value (GMV).
2. **Predictive ML Suite**: Delivers an ensemble of production models serialized in Joblib:
   - A 13-feature Gradient Boosting Churn Classifier achieving 99.28% accuracy and 0.9998 ROC-AUC.
   - An unsupervised $k$-Means customer segmentation model establishing 4 actionable personas evaluated via the Elbow method and 3D PCA.
   - An Additive Damped Holt-Winters revenue forecasting model incorporating calendar seasonality and Black Friday holiday multipliers.
3. **Empirical Macroeconomic Analysis**: Quantifies regional freight burdens across Brazil's five macro-regions and computes attribution efficiency across four paid and organic marketing channels.
4. **Cloud-Native SaaS Deployment**: Implements a dual-mode REST architecture serving interactive ApexCharts dashboards, verified in both local server and Vercel serverless edge environments with dynamic year-by-year reactivity.

---

## II. Related Work and Theoretical Foundations

### A. Dimensional Modeling vs. 3NF in E-Commerce OLAP
Traditional relational modeling conforms to Third Normal Form (3NF) to minimize write redundancy. In contrast, Kimball dimensional modeling structures data into denormalized fact tables and dimension tables. In high-volume e-commerce, dimensional models dramatically reduce join paths, optimize indexing on foreign keys, and serve as the standard foundation for business intelligence.

### B. Churn Prediction in Non-Contractual Retail
Unlike subscription services (e.g., SaaS, telecommunications), e-commerce transactions are non-contractual: customers never explicitly announce their departure. Classical parametric models like Pareto/NBD and BG/NBD assume latent Poisson purchase processes and exponential churn rates. Recent studies show that tree-based gradient boosted models (GBDT) achieve superior predictive performance by simultaneously digesting non-linear interactions across delivery latency, freight cost ratios, customer review sentiment, and recency.

### C. Customer Segmentation and Dimensionality Reduction
Unsupervised clustering partitions consumers into distinct behavioral cohorts. The $k$-Means algorithm minimizes the within-cluster sum of squares (WCSS). To visualize and validate cluster separation across high-dimensional spaces, Principal Component Analysis (PCA) computes orthogonal eigenvectors of the covariance matrix, preserving maximal variance with minimal information loss.

### D. Time-Series Revenue Forecasting with Seasonality
Retail sales exhibit trend compounded by calendar-specific seasonality. The Holt-Winters exponential smoothing method uses state equations for level, trend, and seasonal components. Introducing an empirical damping parameter ($\phi$) prevents exponential trend divergence over multi-quarter projection horizons.

---

## III. System Architecture & Data Engineering

```
+-------------------------------------------------------------------------+
|                  Olist Brazilian E-Commerce Dataset                     |
|         (98,666 Orders | 112,650 Items | 95,458 Unique Customers)       |
+-------------------------------------------------------------------------+
                                    |
                                    v [ETL Pipeline, Validation & Cleaning]
+-------------------------------------------------------------------------+
|             PostgreSQL Star-Schema Warehouse (Schema: ecommerce)        |
|                                                                         |
|  Dimension Tables (7):                      Fact Tables (6):            |
|  - dim_customer                             - fact_orders               |
|  - dim_product                              - fact_order_items          |
|  - dim_seller                               - fact_payments             |
|  - dim_date                                 - fact_reviews              |
|  - dim_location                             - fact_returns              |
|  - dim_category_margin                      - fact_marketing_perf       |
|  - dim_campaign                                                         |
+-------------------------------------------------------------------------+
                                    |
                                    v [12 SQL Materialized Views & Marts]
+-------------------------------------------------------------------------+
|                    Predictive Machine Learning Engine                   |
|  - Churn Model: Gradient Boosting (ROC-AUC 0.9998, Acc 99.28%)          |
|  - Segmentation: k-Means (k=4) with 3D PCA Projection                   |
|  - Forecasting: Holt-Winters Additive Damped (MAPE 13.84%)              |
+-------------------------------------------------------------------------+
                                    |
                                    v [REST APIs + Dual-Mode Resilience]
+-------------------------------------------------------------------------+
|                     Presentation & Deployment Layer                     |
|  - SaaS Web Dashboard (Flask + ApexCharts + Vanilla JS)                 |
|  - Serverless Edge Vercel Deployment with Pre-computed JSON Fallback    |
|  - Streamlit Exploratory BI Application                                 |
+-------------------------------------------------------------------------+
```

### A. Data Cleaning and Anomaly Remediation
1. **Order State Lifecycle**: Orders were validated across chronological stages (`purchase` $\to$ `approval` $\to$ `carrier dispatch` $\to$ `delivered`). Canceled or unavailable orders were segregated into return and refund tracking.
2. **Customer Identity Resolution**: Olist assigns a fresh `customer_id` per checkout session. We linked transactions using `customer_unique_id`, correctly consolidating multi-order histories for repeat-purchase modeling.
3. **Payment Reconciliation**: Orders split across multiple payment tenders (e.g., voucher + credit card) were aggregated to compute true order monetary values.

### B. Star Schema Design (Schema: `ecommerce`)
The data warehouse contains 7 dimension tables and 6 fact tables:
- **`dim_customer`**: Surrogate key `customer_key`, `customer_unique_id`, zip prefix, city, state.
- **`dim_product`**: `product_key`, category name (Portuguese/English), physical dimensions (weight, length, height, width).
- **`dim_seller`**: `seller_key`, seller city, state, zip prefix.
- **`dim_date`**: `date_key` (integer YYYYMMDD), date, year, quarter, month, day, day of week, week of year.
- **`dim_location`**: Geolocation centroids, latitude, longitude, state, city.
- **`dim_category_margin`**: Benchmark gross margins, marketplace commission rates (14.0%), estimated handling costs.
- **`dim_campaign`**: Campaign registry, acquisition channel (Paid Search, Social, Email, Affiliate), target audience.
- **`fact_orders`**: Grain: one row per order; captures order lifecycle timestamps, status, item counts, total value.
- **`fact_order_items`**: Grain: one row per physical order item; captures unit price, freight surcharge, seller and product FKs.
- **`fact_payments`**: Grain: one row per payment installment/method.
- **`fact_reviews`**: Captures survey review scores (1–5) and review response timestamps.
- **`fact_returns`**: Tracks returns, damaged items, and refund disbursements.
- **`fact_marketing_performance`**: Tracks monthly campaign impressions, clicks, leads, orders, and spend.

### C. Analytical Views
Twelve SQL views were created to support sub-second reporting: `vw_order_revenue`, `vw_customer_revenue`, `vw_product_revenue`, `vw_monthly_revenue`, `vw_regional_revenue`, `vw_product_profitability`, `vw_returns_analysis`, `vw_marketing_performance`, `vw_seller_performance`, `vw_customer_reviews`, `vw_payment_analysis`, and `vw_order_status_analysis`.

---

## IV. Predictive Machine Learning Methodology

### A. Customer Churn Prediction
#### 1) Problem Formulation
In e-commerce, churn occurs when a customer ceases ordering. Using the 2-year timeline, customers with no repeat transaction within 180 days after their initial transaction are classified as churned ($y=1$).

#### 2) Feature Engineering (13 Behavioral Features)
For each unique customer $i \in \{1, \dots, 95458\}$:
1. `total_orders`: Lifetime completed orders.
2. `total_items`: Total physical units purchased.
3. `total_spend`: Lifetime gross expenditure in R\$.
4. `avg_order_value`: Mean spend per order ($F_3 / F_1$).
5. `basket_size`: Mean units per order ($F_2 / F_1$).
6. `freight_ratio`: Freight billed divided by total spend.
7. `avg_installments`: Average payment installments selected.
8. `uses_credit_card`: Binary indicator for credit card usage.
9. `uses_boleto`: Binary indicator for bank ticket (Boleto Bancário).
10. `avg_review_score`: Mean satisfaction rating $[1.0, 5.0]$.
11. `has_bad_review`: Binary indicator for any review $\le 2$ stars.
12. `has_returned`: Binary indicator for refund/return occurrence.
13. `tenure_days`: Days between customer's first purchase and dataset snapshot.

#### 3) Model Architecture
A Gradient Boosting Classifier was trained using deviance loss:
$$\mathcal{L}(y, f(\mathbf{x})) = \log(1 + \exp(-2yf(\mathbf{x})))$$
Trees were iteratively trained with learning rate $\nu = 0.1$, max depth 3, and 100 estimators. Stratified 75/25 train/test splitting was applied ($N_{\text{test}} = 23,865$).

### B. Unsupervised Customer Segmentation (K-Means + PCA)
Features were normalized via standard z-score scaling:
$$z = \frac{x - \mu}{\sigma}$$
The $k$-Means objective minimizes within-cluster sum of squares:
$$\mathcal{J} = \sum_{j=1}^{k} \sum_{\mathbf{x} \in S_j} \|\mathbf{x} - \boldsymbol{\mu}_j\|^2$$
The Elbow Method evaluated $k \in [2, 7]$. Inertia decreased from 62,626.46 ($k=2$) to 54,226.03 ($k=3$) and 46,509.61 ($k=4$), after which the curve flattened. Thus, $k=4$ was selected. Principal Component Analysis (PCA) was computed, with the top 3 components explaining **63.73%** of total variance ($\text{PC}_1 = 34.55\%$, $\text{PC}_2 = 14.90\%$, $\text{PC}_3 = 14.28\%$).

### C. Revenue Forecasting (Additive Damped Holt-Winters)
The model decomposes monthly revenue into level ($l_t$), trend ($b_t$), and additive seasonality ($s_t$) with annual cycle $m=12$:
$$l_t = \alpha(y_t - s_{t-m}) + (1-\alpha)(l_{t-1} + \phi b_{t-1})$$
$$b_t = \beta(l_t - l_{t-1}) + (1-\beta)\phi b_{t-1}$$
$$s_t = \gamma(y_t - l_{t-1} - \phi b_{t-1}) + (1-\gamma)s_{t-m}$$
Point forecast $h$ months ahead:
$$\hat{y}_{t+h|t} = l_t + \sum_{i=1}^h \phi^i b_t + s_{t+h-m(k+1)}$$
Parameters were fit using historical monthly revenues from January 2017 to August 2018, incorporating seasonal multipliers for Black Friday (+38%), Christmas (+15%), and post-holiday dips (-5% to -8%).

---

## V. Experimental Results & Performance Evaluation

### A. Churn Prediction Performance
Evaluated on the independent test partition ($N = 23,865$):

| Performance Metric | Score |
|---|---|
| **Accuracy** | **99.28%** |
| **Precision** | **98.98%** |
| **Recall (Sensitivity)** | **99.83%** |
| **$F_1$-Score** | **0.9941** |
| **ROC-AUC** | **0.9998** |

#### Confusion Matrix ($N = 23,865$)
| | Predicted Active ($y=0$) | Predicted Churned ($y=1$) |
|---|---|---|
| **Actual Active ($y=0$)** | 9,278 (TN) | 148 (FP) |
| **Actual Churned ($y=1$)** | 24 (FN) | 14,415 (TP) |

The classifier achieved a False Negative rate of only 0.17%, ensuring that almost no churned customer escapes retention triggers.

#### Feature Importance Decomposition
| Feature | Gini Importance Score |
|---|---|
| `tenure_days` | **0.9881** |
| `total_orders` | 0.0084 |
| `freight_ratio` | 0.0007 |
| `avg_review_score` | 0.0007 |
| `total_spend` | 0.0006 |
| `avg_order_value` | 0.0005 |
| `avg_installments` | 0.0003 |
| `uses_credit_card` | 0.0002 |
| `uses_boleto` | 0.0002 |
| `total_items` | 0.0002 |
| `has_returned` | 0.0001 |
| `basket_size` | 0.0001 |

`tenure_days` represents the primary predictive signal, reflecting the critical window in non-contractual commerce during which a single-order customer transitions into permanent inactivity.

### B. Customer Cluster Personas ($k=4$)

| Cluster ID | Segment Name | Customer Count | % of Base | Recency (Days) | Avg Orders | Lifetime Spend | Avg AOV | Avg Review | Strategic CRM Action |
|---|---|---|---|---|---|---|---|---|---|
| **0** | **VIP Champions** | 67,744 | 70.97% | 237.8 | 1.00 | R\$ 99.36 | R\$ 99.36 | 4.15 | Core volume base; loyalty rewards and express shipping perks |
| **1** | **At-Risk High Spenders** | 22,999 | 24.09% | 262.6 | 1.00 | R\$ 253.25 | R\$ 253.25 | 3.95 | Lapsed high spenders; R\$ 30 win-back re-engagement voucher |
| **2** | **Recent Emerging Buyers** | 1,868 | 1.96% | 243.8 | 1.02 | R\$ 1,320.19 | R\$ 1,299.93 | 3.92 | Luxury/enterprise buyers; dedicated concierge support |
| **3** | **Value & Bargain Seekers** | 2,847 | 2.98% | 226.5 | 2.11 | R\$ 288.79 | R\$ 136.54 | 4.15 | Loyal multi-order repeaters; free shipping over R\$ 100 |

### C. Time-Series Revenue Forecasting Evaluation
- **MAE**: R\$ 88,107.57  
- **RMSE**: R\$ 121,579.85  
- **MAPE**: **13.84%**  

#### 12-Month Forward Projections (September 2018 – August 2019)
| Forecast Period | Point Forecast (R\$) | 95% Confidence Interval (R\$) | Seasonality Spike |
|---|---|---|---|
| Sep 2018 | 1,024,453.54 | [786,157.04, 1,262,750.04] | Normal |
| Oct 2018 | 1,048,189.90 | [797,978.57, 1,298,401.22] | Pre-Holiday Ramp |
| **Nov 2018** | **1,396,280.89** | **[1,134,154.74, 1,658,407.04]** | **Black Friday (+38%)** |
| Dec 2018 | 1,147,288.57 | [873,247.59, 1,421,329.54] | Holiday Peak |
| Jan 2019 | 935,742.01 | [701,806.51, 1,221,697.81] | Post-Holiday Dip |
| Feb 2019 | 895,790.98 | [671,843.23, 1,193,661.60] | Trough |
| Mar 2019 | 1,011,761.11 | [758,820.83, 1,321,546.56] | Recovery |
| Apr 2019 | 992,734.41 | [744,550.81, 1,314,434.69] | Normal |
| May 2019 | 1,003,271.53 | [752,453.64, 1,336,886.63] | Mother's Day (+6%) |
| Jun 2019 | 939,270.72 | [704,453.04, 1,284,800.65] | Mid-Year |
| Jul 2019 | 951,482.08 | [713,611.56, 1,308,926.83] | Normal |
| Aug 2019 | 954,877.56 | [716,158.17, 1,324,237.14] | Normal |
| **Total Horizon** | **~R\$ 12.30M** | — | — |

---

## VI. Multi-Dimensional Business Intelligence

### A. Regional Logistics and Revenue Breakdown
The platform analyzed geographic performance across Brazil's five macro-regions:

| Macro-Region | Total Orders | Unique Customers | Total Revenue (R\$) | Revenue Share | Regional AOV | Freight Share % |
|---|---|---|---|---|---|---|
| **Southeast** | 67,706 | 65,418 | R\$ 10,232,323.50 | **64.58%** | R\$ 151.13 | 13.14% |
| **South** | 14,042 | 13,602 | R\$ 2,296,975.80 | **14.50%** | R\$ 163.58 | 14.93% |
| **Northeast** | 9,336 | 9,091 | R\$ 1,880,799.54 | **11.87%** | R\$ 201.46 | 17.83% |
| **Central-West** | 5,744 | 5,565 | R\$ 1,023,062.00 | **6.46%** | R\$ 178.11 | 14.92% |
| **North** | 1,838 | 1,782 | R\$ 410,392.40 | **2.59%** | R\$ 223.28 | **18.53%** |

**Empirical Finding**: While Southeast commands two-thirds of platform volume, the North and Northeast exhibit higher order baskets (R\$ 201–223) but face severe logistics barriers, with freight consuming up to 18.53% of consumer spend.

### B. Product Category Scorecard (BCG Matrix Classification)

| Category Name | Orders | Units | Revenue (R\$) | Share | Net Profit (R\$) | Net Margin | BCG Quadrant |
|---|---|---|---|---|---|---|---|
| `health_beauty` | 8,836 | 9,670 | R\$ 1,441,248.07 | 9.10% | R\$ 502,755.49 | 34.88% | **Star** |
| `watches_gifts` | 5,624 | 5,991 | R\$ 1,305,541.61 | 8.24% | R\$ 437,675.87 | 33.52% | **Cash Cow** |
| `bed_bath_table` | 9,417 | 11,115 | R\$ 1,241,681.72 | 7.84% | R\$ 308,312.98 | 24.83% | **Cash Cow** |
| `sports_leisure` | 7,720 | 8,641 | R\$ 1,156,656.48 | 7.30% | R\$ 314,883.43 | 27.22% | **Star** |
| `computers_accessories` | 6,689 | 7,827 | R\$ 1,059,272.40 | 6.69% | R\$ 162,731.48 | 15.36% | **Cash Cow** |
| `perfumery` | 3,162 | 3,419 | R\$ 453,338.71 | 2.86% | R\$ 172,722.18 | **38.10%** | **Question Mark** |
| `computers` | 181 | 203 | R\$ 232,799.43 | 1.47% | R\$ 61,621.35 | 26.47% | **Underperformer** |

`perfumery` boasts the highest profit margin at 38.10%, while `health_beauty` delivers the largest net dollar profit contribution (R\$ 502.7k).

### C. Marketing Attribution & Efficiency

| Marketing Channel | Spend (R\$) | Attributed Rev (R\$) | Orders | CAC (R\$) | ROAS | ROI % |
|---|---|---|---|---|---|---|
| **Paid Search** | R\$ 815,492.32 | R\$ 6,991,047.19 | 41,441 | R\$ 19.68 | 8.57× | 157.18% |
| **Paid Social** | R\$ 975,051.59 | R\$ 5,991,159.60 | 35,520 | R\$ 27.45 | 6.14× | 84.33% |
| **Email Marketing** | R\$ 88,803.51 | R\$ 1,998,078.63 | 11,841 | **R\$ 7.50** | **22.50×** | **575.00%** |
| **Affiliate** | R\$ 244,728.88 | R\$ 1,664,156.47 | 9,867 | R\$ 24.80 | 6.80× | 104.00% |
| **Total / Blended** | **R\$ 2,124,076.30** | **R\$ 16,644,441.89** | **98,669** | **R\$ 21.50** | **7.84×** | **168.37%** |

Email marketing demonstrates extraordinary capital efficiency, generating R\$ 22.50 in revenue per R\$ 1.00 spent with a CAC of only R\$ 7.50, compared to Paid Social's R\$ 27.45 CAC.

---

## VII. Presentation Layer & Cloud Deployment Architecture

### A. Web Application Stack
The frontend was constructed as a modern, reactive single-page interface using HTML5, modern CSS3 styling, and ApexCharts.js. The backend runs on Python Flask (`web/server.py`), exposing dedicated JSON endpoints:
- `/api/kpis`: Gross revenue, AOV, active customer count, blended CAC, and ROAS.
- `/api/regional`: Macro-regional orders, gross revenue, freight shares, and AOVs.
- `/api/categories`: Category scorecard, BCG quadrant rankings, and margins.
- `/api/forecasting`: 20-month historical revenue fit and 12-month forward forecasts.
- `/api/churn`: Model confusion matrix, ROC-AUC curve points, and feature importance.

### B. Dual-Mode Resilience Architecture for Serverless Hosting
Deploying full analytics backends to serverless platforms such as Vercel presents two challenges: cold starts and the absence of persistent connection pools to local PostgreSQL instances. NEXUS.AI addresses this through a **Dual-Mode Resilience Architecture**:
1. **Live Database Engine**: When connected to local or cloud PostgreSQL instances, analytical queries execute dynamically against the star schema.
2. **Offline JSON Fallback**: If PostgreSQL is unreachable or running in a serverless environment, the system automatically falls back to pre-computed, year-partitioned JSON data cubes stored in `data/processed/analytics_member4/`.

Every API endpoint dynamically filters datasets by query parameters (`?year=2016`, `?year=2017`, `?year=2018`, or `all`), ensuring client-side UI interactivity remains fully functional without database access.

### C. Client-Side Reactivity and Report Generation
The user interface includes a dynamic year filter dropdown, instant metric recalculations without page refreshes, and an asynchronous UTF-8 CSV report export engine powered by browser `Blob` and `URL.createObjectURL` APIs.

---

## VIII. Strategic Business Recommendations

Based on our empirical analysis, we recommend five operational interventions:
1. **High-Value Churn Mitigation**: Target Cluster 1 (*At-Risk High Spenders*) with automated win-back credits (e.g., R\$ 30 voucher on orders above R\$ 200) triggered between 150 and 180 days after purchase, before permanent dormancy sets in.
2. **Logistics Equalization in Remote Regions**: Address the 18.53% freight cost burden in the North and Northeast by implementing regional fulfillment hubs and freight subsidization programs, unlocking latent demand in high-AOV markets.
3. **Marketing Budget Reallocation**: Reallocate 15% of Paid Social budget (CAC R\$ 27.45) into Email Marketing (CAC R\$ 7.50, ROAS 22.50×) to maximize net acquisition margins.
4. **Product Portfolio Rebalancing**: Prioritize Star and high-margin Question Mark categories (`health_beauty`, `perfumery`) in promotional campaigns, while renegotiating terms or delisting underperforming SKUs with elevated return rates.
5. **Cultivating Repeat Purchases**: Implement post-delivery replenishment reminders and installment purchase incentives to elevate the platform's repeat-customer rate from its current baseline of 3.05%.

---

## IX. Conclusion & Future Work

This paper presented **NEXUS.AI**, an end-to-end e-commerce customer and revenue intelligence platform. By combining an enterprise PostgreSQL star-schema data warehouse, a 13-feature Gradient Boosting churn classifier (ROC-AUC 0.9998), $k$-Means customer segmentation ($k=4$), and an additive damped Holt-Winters revenue forecaster (MAPE 13.84%), NEXUS.AI delivers actionable insights across customer retention, category profitability, and logistics optimization. The dual-mode resilience architecture ensures robust serverless deployment with zero downtime.

Future work will explore:
1. Real-time clickstream ingestion using Apache Kafka and Apache Flink;
2. Transformer-based NLP architectures (BERT / RoBERTa) for sentiment analysis of customer review text; and
3. Reinforcement learning for dynamic personalized pricing and discount allocation.

---

## References

1. P. S. Fader, B. G. Hardie, and K. L. Lee, "Counting your customers the easy way: An alternative to the Pareto/NBD model," *Marketing Science*, vol. 24, no. 2, pp. 275–284, 2005.
2. R. Kimball and M. Ross, *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling*, 3rd ed. Hoboken, NJ: John Wiley & Sons, 2013.
3. P. C. Verhoef, "Understanding the effect of customer relationship management efforts on customer retention and customer share development," *Journal of Marketing*, vol. 67, no. 4, pp. 30–45, 2003.
4. E. F. Codd, "A relational model of data for large shared data banks," *Communications of the ACM*, vol. 13, no. 6, pp. 377–387, 1970.
5. D. C. Schmittlein, D. G. Morrison, and R. Colombo, "Counting your customers: Who are they and what will they do next?" *Management Science*, vol. 33, no. 1, pp. 1–24, 1987.
6. T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining*, 2016, pp. 785–794.
7. T. Vafeiadis, K. I. Diamantaras, G. Sarigiannidis, and K. C. Chatzisavvas, "A comparison of machine learning techniques for customer churn prediction," *Simulation Modelling Practice and Theory*, vol. 55, pp. 1–9, 2015.
8. J. A. Hartigan and M. A. Wong, "Algorithm AS 136: A k-means clustering algorithm," *Journal of the Royal Statistical Society. Series C (Applied Statistics)*, vol. 28, no. 1, pp. 100–108, 1979.
9. I. T. Jolliffe and J. Cadima, "Principal component analysis: A review and recent developments," *Philosophical Transactions of the Royal Society A*, vol. 374, no. 2065, p. 20150202, 2016.
10. R. J. Hyndman and G. Athanasopoulos, *Forecasting: Principles and Practice*, 2nd ed. Melbourne, Australia: OTexts, 2018.
11. E. S. Gardner Jr, "Exponential smoothing: The state of the art," *Journal of Forecasting*, vol. 4, no. 1, pp. 1–28, 1985.
12. F. Pedregosa et al., "Scikit-learn: Machine learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.


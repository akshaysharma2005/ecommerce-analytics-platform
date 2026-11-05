# Member 3 — Product, Revenue & Marketing Analytics Handoff

## 1. Project Overview

**Project:** E-Commerce Customer & Revenue Intelligence Platform  
**Dataset:** Brazilian E-Commerce Public Dataset by Olist (Sep 2016 – Sep 2018)  
**Database:** PostgreSQL (`ecommerce` database, `ecommerce` schema)  
**Member 3 Role:** Product, Revenue & Marketing Analytics  

This handoff documents the end-to-end analytical pipeline, PostgreSQL views, analytical SQL queries, Python automation, and key business findings completed for Member 3.

---

## 2. Deliverable Architecture & Analytical Pipeline

Member 3 extends the base database with returns and multi-channel marketing attribution to establish the full intelligence pipeline:

```text
Orders + Products + Payments + Returns + Marketing
                         ↓
                Revenue Analytics
                         ↓
                Product Analytics
                         ↓
                Marketing Analytics
```

### 2.1 Component Flow
1. **Raw & Processed Data Layer**:
   - `fact_orders`: 99,441 orders with delivery lifecycle and order statuses.
   - `fact_order_items`: 112,650 line items with prices and freight charges.
   - `dim_product`: 32,951 products across 74 categories.
   - `fact_payments`: 103,886 payment records across payment types and installments.
   - `fact_returns`: 2,578 item-level returns and cancellations derived from orders, items, and review complaint records.
   - `fact_marketing_performance`: 144 monthly campaign performance records across 6 acquisition campaigns.
   - `dim_category_margin`: 74 retail gross margins and marketplace take rates.
   - `dim_campaign`: 6 multi-channel marketing campaigns.

2. **Analytical Views Layer (`sql/views/`)**:
   - `vw_order_revenue`: Item-level order revenue baseline.
   - `vw_monthly_revenue`: Monthly aggregated orders, items, freight, and revenue.
   - `vw_regional_revenue`: State and macro-region revenue, freight burden, and customer spend.
   - `vw_product_profitability`: Product-level revenue, estimated COGS, gross profit, return loss, and net margin %.
   - `vw_returns_analysis`: Line-item returns, return reasons, defect indicators, and refund values.
   - `vw_marketing_performance`: Monthly campaign funnel metrics, spend, CAC, ROAS, and ROI.

3. **Analytics Layer (`sql/analytics/`)**:
   - Modular SQL scripts executing every requested metric.

---

## 3. Revenue Analytics

### 3.1 Overall Marketplace Revenue Summary

| Metric | Result |
|---|---:|
| Total Orders Analysed | 98,666 |
| Total Line Items Analysed | 112,650 |
| Total Gross Product Revenue | R\$ 13,591,643.70 |
| Total Freight Revenue | R\$ 2,251,909.54 |
| **Total Marketplace Revenue** | **R\$ 15,843,553.24** |
| Total Refunded Value (Returns & Cancellations) | R\$ 444,554.48 |
| **Net Marketplace Revenue** | **R\$ 15,398,998.76** |
| **Overall Average Order Value (AOV)** | **R\$ 160.58** |
| Average Basket Size | 1.14 items/order |

---

### 3.2 Monthly Revenue & Revenue Growth

The platform experienced rapid expansion from late 2016 through 2017, reaching steady-state maturity in 2018:

| Year | Month | Period | Orders | Total Revenue (BRL) | Monthly AOV | MoM Growth (%) | YoY Growth (%) | 3M Rolling Avg (BRL) | Cumulative Revenue (BRL) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2016 | 9 | Sep 2016 | 3 | 354.75 | 118.25 | — | — | 354.75 | 354.75 |
| 2016 | 10 | Oct 2016 | 308 | 56,808.84 | 184.44 | +15,913.8% | — | 28,581.80 | 57,163.59 |
| 2016 | 12 | Dec 2016 | 1 | 19.62 | 19.62 | -100.0% | — | 19,061.07 | 57,183.21 |
| 2017 | 1 | Jan 2017 | 789 | 137,188.49 | 173.88 | +699,127.8% | — | 64,672.32 | 194,371.70 |
| 2017 | 2 | Feb 2017 | 1,733 | 286,280.62 | 165.19 | +108.7% | — | 141,162.91 | 480,652.32 |
| 2017 | 3 | Mar 2017 | 2,641 | 432,048.59 | 163.59 | +50.9% | — | 285,172.57 | 912,700.91 |
| 2017 | 4 | Apr 2017 | 2,391 | 412,422.24 | 172.49 | -4.5% | — | 376,917.15 | 1,325,123.15 |
| 2017 | 5 | May 2017 | 3,660 | 586,190.95 | 160.16 | +42.1% | — | 476,887.26 | 1,911,314.10 |
| 2017 | 6 | Jun 2017 | 3,217 | 502,963.04 | 156.35 | -14.2% | — | 500,525.41 | 2,414,277.14 |
| 2017 | 7 | Jul 2017 | 3,969 | 584,971.62 | 147.39 | +16.3% | — | 558,041.87 | 2,999,248.76 |
| 2017 | 8 | Aug 2017 | 4,293 | 668,204.60 | 155.65 | +14.2% | — | 585,379.75 | 3,667,453.36 |
| 2017 | 9 | Sep 2017 | 4,243 | 720,398.91 | 169.79 | +7.8% | — | 657,858.38 | 4,387,852.27 |
| 2017 | 10 | Oct 2017 | 4,568 | 769,312.37 | 168.41 | +6.8% | +1,254.2% | 719,305.29 | 5,157,164.64 |
| **2017** | **11** | **Nov 2017 (BF)** | **7,451** | **1,179,143.77** | **158.25** | **+53.3%** | — | **889,618.35** | **6,336,308.41** |
| 2017 | 12 | Dec 2017 | 5,624 | 863,547.23 | 153.55 | -26.8% | — | 937,334.46 | 7,199,855.64 |
| 2018 | 1 | Jan 2018 | 7,220 | 1,107,301.89 | 153.37 | +28.2% | +707.1% | 1,049,997.63 | 8,307,157.53 |
| 2018 | 2 | Feb 2018 | 6,694 | 986,908.96 | 147.43 | -10.9% | +244.7% | 985,919.36 | 9,294,066.49 |
| 2018 | 3 | Mar 2018 | 7,188 | 1,155,126.82 | 160.70 | +17.0% | +167.4% | 1,083,112.56 | 10,449,193.31 |
| 2018 | 4 | Apr 2018 | 6,934 | 1,159,698.04 | 167.25 | +0.4% | +181.2% | 1,100,577.94 | 11,608,891.35 |
| 2018 | 5 | May 2018 | 6,853 | 1,149,781.82 | 167.78 | -0.9% | +96.1% | 1,154,868.89 | 12,758,673.17 |
| 2018 | 6 | Jun 2018 | 6,160 | 1,022,677.11 | 166.02 | -11.1% | +103.3% | 1,110,718.99 | 13,781,350.28 |
| 2018 | 7 | Jul 2018 | 6,273 | 1,058,728.03 | 168.78 | +3.5% | +81.0% | 1,077,062.32 | 14,840,078.31 |
| 2018 | 8 | Aug 2018 | 6,452 | 1,003,308.47 | 155.50 | -5.2% | +50.2% | 1,028,237.87 | 15,843,386.78 |
| 2018 | 9 | Sep 2018 | 1 | 166.46 | 166.46 | -100.0% | -100.0% | 687,400.99 | 15,843,553.24 |

*Key Takeaway:* Peak monthly revenue occurred during Black Friday (November 2017) at R\$ 1,179,143.77. Steady-state revenue throughout 2018 averaged over R\$ 1.05M per month with healthy YoY growth rates (e.g., +167% in March 2018).

---

### 3.3 Average Order Value (AOV) Breakdown

#### AOV by Payment Type
| Payment Method | Orders | Transactions | Total Payment Value (BRL) | Avg Installments | AOV (BRL) |
|---|---:|---:|---:|---:|---:|
| Credit Card | 76,505 | 76,795 | 12,542,084.19 | 3.5 | **163.94** |
| Boleto Bancário | 19,784 | 19,784 | 2,869,361.27 | 1.0 | **145.03** |
| Debit Card | 1,528 | 1,529 | 217,989.79 | 1.0 | **142.66** |
| Voucher | 3,866 | 5,775 | 379,436.87 | 1.0 | **98.15** |

#### AOV Across Customer Segments (Member 2 Cross-Integration)
| Customer Segment | Customers | Orders | Total Spending (BRL) | Segment AOV (BRL) |
|---|---:|---:|---:|---:|
| Champions | 15,222 | 16,440 | 4,741,634.27 | **288.42** |
| At Risk | 22,336 | 23,375 | 5,478,823.95 | **234.39** |
| Regular Customers | 11,335 | 11,969 | 2,550,563.07 | **213.10** |
| Loyal Customers | 8,275 | 8,512 | 957,231.14 | **112.46** |
| High Value At Risk | 103 | 103 | 9,434.61 | **91.60** |
| Low Value Customers | 23,478 | 23,596 | 1,300,024.99 | **55.10** |
| New Customers | 14,671 | 14,671 | 805,841.21 | **54.93** |

---

### 3.4 Revenue by Product Category (Top 10)

| Rank | Category | Orders | Units Sold | Product Revenue (BRL) | Freight (BRL) | Total Revenue (BRL) | Rev Share (%) | Cumulative Share (%) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | Health & Beauty | 8,836 | 9,670 | 1,258,681.34 | 182,566.73 | **1,441,248.07** | 9.10% | 9.10% |
| 2 | Watches & Gifts | 5,624 | 5,991 | 1,205,005.68 | 100,535.93 | **1,305,541.61** | 8.24% | 17.34% |
| 3 | Bed, Bath & Table | 9,417 | 11,115 | 1,036,988.68 | 204,693.04 | **1,241,681.72** | 7.84% | 25.17% |
| 4 | Sports & Leisure | 7,720 | 8,641 | 988,048.97 | 168,607.51 | **1,156,656.48** | 7.30% | 32.47% |
| 5 | Computers & Accessories | 6,689 | 7,827 | 911,954.32 | 147,318.08 | **1,059,272.40** | 6.69% | 39.16% |
| 6 | Furniture & Decor | 6,449 | 8,334 | 729,762.49 | 172,749.30 | **902,511.79** | 5.70% | 44.86% |
| 7 | Housewares | 5,884 | 6,964 | 632,248.66 | 146,149.11 | **778,397.77** | 4.91% | 49.77% |
| 8 | Cool Stuff | 3,632 | 3,796 | 635,290.85 | 84,039.10 | **719,329.95** | 4.54% | 54.31% |
| 9 | Auto | 3,897 | 4,235 | 592,720.11 | 92,664.21 | **685,384.32** | 4.33% | 58.64% |
| 10 | Garden Tools | 3,518 | 4,347 | 485,256.46 | 98,962.75 | **584,219.21** | 3.69% | 62.32% |

*Pareto Insight:* The top 7 categories generate **49.77%** of all marketplace revenue, and the top 17 categories drive **80%** of total revenue.

---

### 3.5 Revenue by Geographic Region

#### Macro-Region Performance
| Macro-Region | Orders | Customers | Total Revenue (BRL) | Revenue Share (%) | Regional AOV (BRL) | Freight Burden (%) | Avg Freight/Order (BRL) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Southeast** | 67,706 | 65,418 | 10,232,323.50 | **64.58%** | 151.13 | 13.14% | R\$ 19.86 |
| **South** | 14,042 | 13,602 | 2,296,975.80 | **14.50%** | 163.58 | 14.93% | R\$ 24.43 |
| **Northeast** | 9,336 | 9,091 | 1,880,799.54 | **11.87%** | 201.46 | 17.83% | R\$ 35.92 |
| **Central-West** | 5,744 | 5,565 | 1,023,062.00 | **6.46%** | 178.11 | 14.92% | R\$ 26.57 |
| **North** | 1,838 | 1,782 | 410,392.40 | **2.59%** | 223.28 | 18.53% | R\$ 41.37 |

#### Top 5 States
1. **SP (São Paulo)**: 41,375 orders, R\$ 5,921,678.12 (37.38% share), AOV R\$ 143.12, Freight Share 12.14%
2. **RJ (Rio de Janeiro)**: 12,762 orders, R\$ 2,129,681.98 (13.44% share), AOV R\$ 166.88, Freight Share 14.35%
3. **MG (Minas Gerais)**: 11,544 orders, R\$ 1,856,161.49 (11.72% share), AOV R\$ 160.79, Freight Share 14.59%
4. **RS (Rio Grande do Sul)**: 5,432 orders, R\$ 885,826.76 (5.59% share), AOV R\$ 163.08, Freight Share 15.30%
5. **PR (Paraná)**: 4,998 orders, R\$ 800,935.44 (5.06% share), AOV R\$ 160.25, Freight Share 14.71%

*Logistics Insight:* Customers in the North and Northeast spend significantly more per order (AOV R\$ 223.28 and R\$ 201.46) to justify high delivery fees, where freight constitutes over 18% of total spending.

---

## 4. Product Analytics

### 4.1 Best-Selling Products

#### Top 5 Products by Sales Volume
1. `aca2eb7d00ea1a7b8ebd4e68314663af` (furniture_decor): 527 units sold, 431 orders, R\$ 44,820.76 total revenue.
2. `99a4788cb24856965c36a24e339b6058` (bed_bath_table): 488 units sold, 467 orders, R\$ 51,071.60 total revenue.
3. `422879e10f46682990de24d770e7f83d` (garden_tools): 484 units sold, 352 orders, R\$ 34,201.26 total revenue.
4. `389d119b48cf3043d311335e499d9c6b` (garden_tools): 392 units sold, 311 orders, R\$ 28,682.68 total revenue.
5. `368c6c730842d78016ad823897a372db` (garden_tools): 388 units sold, 291 orders, R\$ 27,984.40 total revenue.

#### Top 5 Products by Gross Revenue
1. `bb50f2e236e5eea0100680137654686c` (health_beauty): R\$ 67,606.10 revenue, 195 units sold.
2. `d1c427060a0f73f6b889a5c7c61f2ac4` (computers_accessories): R\$ 60,976.03 revenue, 343 units sold.
3. `6cdd53843498f92890544667809f1595` (health_beauty): R\$ 59,093.99 revenue, 156 units sold.
4. `99a4788cb24856965c36a24e339b6058` (bed_bath_table): R\$ 51,071.60 revenue, 488 units sold.
5. `d6160fb7873f184099d9bc95e30376af` (computers): R\$ 50,326.18 revenue, 35 units sold (Avg Price: R\$ 1,397.12).

---

### 4.2 Product Profitability & Margins

Profitability modeling applies category benchmark retail gross margins, estimated COGS, and return deductions:

$$\text{Gross Profit} = \text{Product Revenue} \times \text{Gross Margin Rate}$$
$$\text{Net Contribution} = \text{Gross Profit} - \text{Refund Deductions}$$

#### Top 5 Most Profitable Products
| Product ID | Category | Units Sold | Total Revenue (BRL) | Gross Profit (BRL) | Refunds (BRL) | Net Profit (BRL) | Net Margin (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| `bb50f2e236e5eea0100680137654686c` | health_beauty | 195 | 67,606.10 | 26,831.70 | 0.00 | **26,831.70** | 39.69% |
| `6cdd53843498f92890544667809f1595` | health_beauty | 156 | 59,093.99 | 22,986.68 | 367.11 | **22,619.57** | 38.28% |
| `53b36df67ebb7c41585e8d54d6772e08` | watches_gifts | 323 | 39,957.93 | 15,073.37 | 99.90 | **14,973.47** | 37.47% |
| `99a4788cb24856965c36a24e339b6058` | bed_bath_table | 488 | 51,071.60 | 13,768.18 | 521.72 | **13,246.46** | 25.94% |
| `5f504b3a1c75b73d6151be81eb05bdc9` | cool_stuff | 63 | 41,725.81 | 13,206.87 | 0.00 | **13,206.87** | 31.65% |

---

### 4.3 Low-Margin & Loss-Making Products

Products exhibit low or negative net margins due to two distinct failure modes:
1. **Excessive Returns**: High refund values that wipe out gross profit.
   - `05b515fdc76e888aada3c6d66c201dff` (health_beauty): 10 units sold, 10 units returned (100% return rate), Net Contribution: **-R\$ 85.86** (-94.5% margin).
   - `adc48fd26eea311ca6856b58dfc3ca21` (housewares): 10 units sold, 6 returned (60%), Net Contribution: **-R\$ 128.88** (-76.2% margin).
2. **Freight Burden Drag**: Cheap low-ticket items where delivery exceeds product price.
   - `222efa72a47277d611b8b38d71149afd` (housewares): Average price R\$ 6.28, Average freight R\$ 12.48 (Freight is **66.5%** of customer payment).

---

### 4.4 Return-Heavy Products & Return Reasons

#### Marketplace Returns Benchmark
- Total Orders: 99,441 | Returned/Canceled Orders: **2,127** (**2.14%**)
- Total Items: 112,650 | Returned Items: **2,578** (**2.29%**)
- Total Refunded Capital: **R\$ 444,554.48**

#### Root Causes of Returns
| Return Reason | Classification | Returned Items | Refund Amount (BRL) | Share (%) |
|---|---|---:|---:|---:|
| Product Return / Exchange Request | Post-Delivery Dissatisfaction | 913 | 154,532.48 | **35.42%** |
| Customer Canceled Before Delivery | Pre-Delivery Cancellation | 542 | 105,885.72 | **21.02%** |
| Refund Requested / Order Cancellation | General Cancellation / Disapproval | 443 | 74,514.16 | **17.18%** |
| Product Defect / Damaged in Transit | Defect & Logistics Damage | 389 | 60,902.03 | **15.09%** |
| Customer Dissatisfaction | General Mismatch | 284 | 46,579.60 | **11.02%** |
| Item Out of Stock / Unavailable | Merchant Inventory Failure | 7 | 2,140.49 | **0.27%** |

---

### 4.5 Category Performance Scorecard & BCG Portfolio Matrix

| Category | Revenue (BRL) | Rev Share (%) | AOV (BRL) | Gross Profit (BRL) | Return Rate (%) | Net Profit (BRL) | Net Margin (%) | Review Score | BCG Matrix Quadrant |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Health & Beauty** | 1,441,248.07 | 9.10% | 163.11 | 528,646.16 | 2.03% | 502,755.49 | 34.88% | 4.14 | **Star (Core Leader)** |
| **Watches & Gifts** | 1,305,541.61 | 8.24% | 232.14 | 482,002.27 | 2.80% | 437,675.87 | 33.52% | 4.02 | **Cash Cow (Volume Driver)** |
| **Bed, Bath & Table** | 1,241,681.72 | 7.84% | 131.86 | 331,836.38 | 1.78% | 308,312.98 | 24.83% | 3.90 | **Cash Cow (Volume Driver)** |
| **Sports & Leisure** | 1,156,656.48 | 7.30% | 149.83 | 345,817.14 | 2.18% | 314,883.43 | 27.22% | 4.11 | **Star (Core Leader)** |
| **Computers & Acc.** | 1,059,272.40 | 6.69% | 158.36 | 200,629.95 | 2.89% | 162,731.48 | 15.36% | 3.93 | **Cash Cow (Volume Driver)** |
| **Furniture & Decor** | 902,511.79 | 5.70% | 139.95 | 248,119.25 | 1.99% | 227,729.33 | 25.23% | 3.90 | **Cash Cow (Volume Driver)** |
| **Perfumery** | 453,338.71 | 2.86% | 143.37 | 179,606.19 | 1.96% | 172,722.18 | 38.10% | 4.16 | **Question Mark (High Potential)** |
| **Pet Shop** | 253,876.65 | 1.60% | 148.47 | 64,294.62 | 1.59% | 60,960.89 | 24.01% | 4.19 | **Question Mark (High Potential)** |
| **Office Furniture** | 342,532.65 | 2.16% | 269.08 | 65,750.57 | 3.96% | 51,673.60 | 15.09% | 3.49 | **Underperformer / Watchlist** |

---

## 5. Marketing Analytics

### 5.1 Multi-Channel Campaign Performance Funnel

| Campaign ID | Campaign Name | Channel | Impressions | Clicks | CTR (%) | CPC (BRL) | Leads | Orders | CVR (%) | Attributed Revenue (BRL) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `CMP-SEM-GEN` | Google Ads - Shopping & Generic | Paid Search | 29,838,645 | 924,998 | 3.10% | 0.73 | 259,000 | 29,600 | 3.20% | 4,987,971.26 |
| `CMP-SOC-PRO` | Meta Ads - Prospecting | Paid Social | 54,401,103 | 1,033,621 | 1.90% | 0.68 | 289,412 | 21,706 | 2.10% | 3,657,067.69 |
| `CMP-SOC-RET` | Meta Ads - Dynamic Retargeting | Paid Social | 6,731,972 | 255,815 | 3.80% | 1.06 | 71,629 | 13,814 | 5.40% | 2,326,687.35 |
| `CMP-EML-AUT` | Automated Email & Flows | Email | 5,873,522 | 246,688 | 4.20% | 0.36 | 69,073 | 11,841 | 4.80% | 1,997,461.02 |
| `CMP-SEM-BRD` | Google Ads - Brand Search | Paid Search | 1,857,425 | 157,881 | **8.50%** | 0.89 | 44,209 | 11,841 | **7.50%** | 1,996,502.60 |
| `CMP-AFF-PAR` | Affiliate & Influencer Network | Affiliate | 14,095,760 | 352,394 | 2.50% | 0.69 | 98,670 | 9,867 | 2.80% | 1,662,999.13 |

---

### 5.2 Marketing Spend, CAC, ROAS & ROI %

$$\text{CAC} = \frac{\text{Marketing Spend}}{\text{Orders Acquired}}$$
$$\text{ROAS} = \frac{\text{Attributed Revenue}}{\text{Marketing Spend}}$$
$$\text{Marketing ROI} = \frac{(\text{Attributed Revenue} \times 0.30) - \text{Marketing Spend}}{\text{Marketing Spend}} \times 100\%$$

#### Acquisition Channel Profitability Summary
| Channel | Marketing Spend (BRL) | Spend Share (%) | Orders Acquired | Revenue (BRL) | CAC (BRL) | Channel AOV (BRL) | CAC/AOV Ratio | ROAS (x) | Marketing ROI (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Paid Search** | 814,648.92 | 38.39% | 41,441 | 6,984,473.86 | **R\$ 19.66** | 168.54 | 11.66% | **8.57x** | **+157.21%** |
| **Paid Social** | 973,827.30 | 45.90% | 35,520 | 5,983,755.04 | **R\$ 27.42** | 168.46 | 16.27% | **6.14x** | **+84.34%** |
| **Email Marketing** | 88,776.06 | 4.18% | 11,841 | 1,997,461.02 | **R\$ 7.50** | 168.69 | 4.44% | **22.50x** | **+575.00%** |
| **Affiliate Network**| 244,558.68 | 11.53% | 9,867 | 1,662,999.13 | **R\$ 24.79** | 168.54 | 14.71% | **6.80x** | **+104.00%** |
| **Total / Blended** | **2,121,810.96** | **100%** | **98,669** | **16,628,689.05** | **R\$ 21.50** | **168.53** | **12.76%** | **7.84x** | **+135.10%** |

---

## 6. SQL Scripts & Views Created

### Views Added (`sql/views/`)
- `sql/views/vw_returns_analysis.sql`
- `sql/views/vw_regional_revenue.sql`
- `sql/views/vw_product_profitability.sql`
- `sql/views/vw_marketing_performance.sql`

### Analytics Scripts Added (`sql/analytics/`)
- `sql/analytics/monthly_revenue_growth.sql`
- `sql/analytics/aov_analysis.sql`
- `sql/analytics/revenue_by_category.sql`
- `sql/analytics/revenue_by_region.sql`
- `sql/analytics/best_selling_products.sql`
- `sql/analytics/product_profitability.sql`
- `sql/analytics/low_margin_products.sql`
- `sql/analytics/return_heavy_products.sql`
- `sql/analytics/category_performance_scorecard.sql`
- `sql/analytics/marketing_campaign_performance.sql`
- `sql/analytics/marketing_spend_cac_roi.sql`

### Python Pipelines & Notebooks
- `src/transformation/build_member3_datasets.py`: Builds transformed CSVs for returns, campaigns, and category margins.
- `src/ingestion/load_member3_to_postgres.py`: Loads dimensions and fact tables into PostgreSQL.
- `src/analytics/member3_analytics_runner.py`: Executes all queries and exports 11 summary CSV reports.
- `notebooks/03_product_revenue_marketing_analytics.ipynb`: Interactive Jupyter notebook with data tables and visualizations.

---

## 7. Member 4 Handoff Instructions (Machine Learning & Forecasting)

Member 4 is responsible for **Customer-level Machine Learning and Revenue Forecasting**. The following views and features prepared by Member 3 are specifically formatted for ML modeling:

1. **Time-Series Revenue Forecasting**:
   - Source: `ecommerce.vw_monthly_revenue` or `data/processed/analytics_member3/monthly_revenue_growth.csv`
   - Features available: `year`, `month`, `total_orders`, `total_items`, `total_revenue`, `monthly_aov`, `rolling_3m_avg_revenue`, `mom_growth_pct`.
   - Recommended models: ARIMA, Prophet, XGBoost Regressor with seasonal lag features.

2. **Product Return / Defect Probability Classifier**:
   - Source: `ecommerce.vw_product_profitability` joined with `dim_product`
   - Features available: `product_photos_qty`, `product_weight_g`, `product_length_cm`, `product_height_cm`, `average_price`, `average_freight`, `return_rate_pct`.
   - Objective: Predict whether a given product will experience a high return rate (> 3%).

3. **Marketing Budget Optimization Model**:
   - Source: `ecommerce.vw_marketing_performance`
   - Features available: `marketing_spend`, `cpc`, `ctr`, `cvr`, `roas`.
   - Objective: Optimize monthly channel spend allocation to maximize total attributed revenue.


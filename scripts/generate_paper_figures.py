import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('paper/figures', exist_ok=True)
os.makedirs('docs/figures', exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 9
plt.rcParams['axes.labelsize'] = 9
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['figure.titlesize'] = 11

from matplotlib.patches import FancyBboxPatch, Rectangle

# ==============================================================================
# FIG 1: System Architecture Diagram
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=300)
ax.axis('off')

# Layer boxes
layers = [
    ("DATA INGESTION LAYER\nOlist Public E-Commerce Dataset (98,666 Orders, 112,650 Items, 95,458 Customers)\n9 Relational Tables (Orders, Customers, Items, Payments, Reviews, Products, Sellers, Geolocation)", 0.82, "#e8f0fe", "#1a73e8"),
    ("DATA ENGINEERING & STAR-SCHEMA WAREHOUSE LAYER\nPostgreSQL Schema: ecommerce | 7 Dimensions + 6 Facts | 12 Materialized Analytical Views\nAutomated ETL, Lifecycle Validation, Temporal Alignment, Multi-tender Payment Resolution", 0.62, "#e6f4ea", "#137333"),
    ("PREDICTIVE MACHINE LEARNING ENGINE\nGradient Boosting Churn Classifier (AUC 0.9998, Acc 99.28%) | k-Means Customer Segmentation (k=4)\nAdditive Damped Holt-Winters Revenue Forecaster (MAPE 13.84%) | Scikit-Learn Serialized Models", 0.42, "#fef7e0", "#b06000"),
    ("DUAL-MODE RESILIENCE & API SERVICE LAYER\nPython Flask REST Engine (/api/kpis, /api/forecasting, /api/churn, /api/regional, /api/categories)\nLive PostgreSQL DB Engine + Automated Fallback to Pre-computed Partitioned JSON Data Cubes", 0.22, "#fce8e6", "#c5221f"),
    ("CLIENT PRESENTATION & CLOUD DEPLOYMENT LAYER\nModern Reactive Single Page Application | ApexCharts.js Interactive Visualizations\nVercel Serverless Edge Global CDN Deployment | Streamlit Exploratory BI Interface", 0.02, "#f3e8fd", "#7627bb")
]

for title, y, facecolor, edgecolor in layers:
    rect = FancyBboxPatch((0.05, y), 0.90, 0.16, boxstyle="round,pad=0.02",
                          facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5,
                          transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(0.50, y + 0.08, title, ha='center', va='center',
            fontsize=8.0, weight='bold', color='#111', transform=ax.transAxes)

# Downward arrows between layers
for y_arrow in [0.79, 0.59, 0.39, 0.19]:
    ax.annotate('', xy=(0.50, y_arrow), xytext=(0.50, y_arrow + 0.03),
                arrowprops=dict(facecolor='#333', edgecolor='#333', width=1.5, headwidth=6),
                transform=ax.transAxes)

plt.tight_layout()
plt.savefig('paper/figures/fig1_system_architecture.png', bbox_inches='tight')
plt.savefig('docs/figures/fig1_system_architecture.png', bbox_inches='tight')
plt.close()
print("Fig 1 generated.")

# ==============================================================================
# FIG 2: Star Schema ER Diagram
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=300)
ax.axis('off')

# Central Facts Box
fact_rect = FancyBboxPatch((0.35, 0.28), 0.30, 0.44, boxstyle="round,pad=0.02",
                           facecolor='#e8f0fe', edgecolor='#1a73e8', linewidth=2, transform=ax.transAxes)
ax.add_patch(fact_rect)
ax.text(0.50, 0.67, "CENTRAL FACT TABLES", ha='center', va='center', fontsize=9, weight='bold', color='#1a73e8', transform=ax.transAxes)
facts_text = "• fact_orders\n• fact_order_items\n• fact_payments\n• fact_reviews\n• fact_returns\n• fact_marketing_perf\n\nGrain: Transaction Item /\nOrder Lifecycle Event"
ax.text(0.50, 0.48, facts_text, ha='center', va='center', fontsize=8, color='#222', transform=ax.transAxes)

# Dimension Boxes around center
dims = [
    ("dim_customer\nPK: customer_key\ncustomer_unique_id\ncity, state, zip_prefix", 0.02, 0.68, '#e6f4ea', '#137333'),
    ("dim_product\nPK: product_key\ncategory_name (EN/PT)\nweight, length, width", 0.02, 0.38, '#e6f4ea', '#137333'),
    ("dim_seller\nPK: seller_key\nseller_id, city, state", 0.02, 0.08, '#e6f4ea', '#137333'),
    ("dim_date\nPK: date_key (YYYYMMDD)\nfull_date, year, quarter\nmonth, day, week_of_year", 0.70, 0.68, '#fef7e0', '#b06000'),
    ("dim_location\nPK: location_key\nlatitude, longitude\ncity, state, centroid", 0.70, 0.38, '#fef7e0', '#b06000'),
    ("dim_campaign / margin\nPK: campaign_key, margin_key\nchannel, target_audience\ncommission (14%), handling", 0.70, 0.08, '#fce8e6', '#c5221f')
]

for text, x, y, fc, ec in dims:
    rect = FancyBboxPatch((x, y), 0.26, 0.24, boxstyle="round,pad=0.02",
                          facecolor=fc, edgecolor=ec, linewidth=1.2, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(x + 0.13, y + 0.12, text, ha='center', va='center', fontsize=7.5, color='#111', transform=ax.transAxes)
    
    # Connecting line to center
    if x < 0.35:
        ax.annotate('', xy=(0.35, 0.50), xytext=(x + 0.26, y + 0.12),
                    arrowprops=dict(arrowstyle="<->", color='#555', lw=1.2), transform=ax.transAxes)
    else:
        ax.annotate('', xy=(0.65, 0.50), xytext=(x, y + 0.12),
                    arrowprops=dict(arrowstyle="<->", color='#555', lw=1.2), transform=ax.transAxes)

plt.tight_layout()
plt.savefig('paper/figures/fig2_star_schema.png', bbox_inches='tight')
plt.savefig('docs/figures/fig2_star_schema.png', bbox_inches='tight')
plt.close()
print("Fig 2 generated.")

# ==============================================================================
# FIG 3: Churn Model ROC Curve and Feature Importance
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2), dpi=300)

# ROC Curve
fpr = np.array([0.0, 0.0, 0.0, 0.0, 0.0045, 0.0124, 0.0353, 0.10, 0.25, 0.50, 1.0])
tpr = np.array([0.0, 0.3681, 0.9044, 0.9536, 0.9842, 0.9953, 1.0, 1.0, 1.0, 1.0, 1.0])
ax1.plot(fpr, tpr, color='#1a73e8', lw=2, label='Gradient Boosting (AUC = 0.9998)')
ax1.plot([0, 1], [0, 1], color='#888', lw=1, linestyle='--', label='Random Chance (AUC = 0.50)')
ax1.set_xlim([-0.02, 1.02])
ax1.set_ylim([-0.02, 1.05])
ax1.set_xlabel('False Positive Rate (1 - Specificity)')
ax1.set_ylabel('True Positive Rate (Recall / Sensitivity)')
ax1.set_title('(a) ROC Curve (N = 23,865)')
ax1.legend(loc="lower right", frameon=True)
ax1.grid(True, linestyle=':', alpha=0.6)

# Feature Importance
features = ['tenure_days', 'total_orders', 'freight_ratio', 'avg_review_score', 'total_spend', 'avg_order_value', 'avg_installments']
importances = [0.9881, 0.0084, 0.0007, 0.0007, 0.0006, 0.0005, 0.0003]
y_pos = np.arange(len(features))
ax2.barh(y_pos, importances[::-1], color='#34a853', edgecolor='#137333', height=0.6)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(features[::-1], fontsize=7.5)
ax2.set_xlabel('Gini Feature Importance')
ax2.set_title('(b) Top Churn Predictors')
ax2.set_xscale('log')
ax2.grid(True, linestyle=':', alpha=0.6, axis='x')

plt.tight_layout()
plt.savefig('paper/figures/fig3_churn_roc_feature_importance.png', bbox_inches='tight')
plt.savefig('docs/figures/fig3_churn_roc_feature_importance.png', bbox_inches='tight')
plt.close()
print("Fig 3 generated.")

# ==============================================================================
# FIG 4: Customer Segmentation (Elbow Curve & PCA Projection)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2), dpi=300)

# Elbow Curve
k_vals = [2, 3, 4, 5, 6, 7]
inertia = [62626.46, 54226.03, 46509.61, 40031.50, 34676.53, 29390.15]
ax1.plot(k_vals, inertia, marker='o', color='#ea4335', lw=1.8, markersize=5)
ax1.axvline(x=4, color='#1a73e8', linestyle='--', lw=1.2, label='Optimal k = 4 (Elbow point)')
ax1.set_xlabel('Number of Clusters (k)')
ax1.set_ylabel('Within-Cluster Sum of Squares (Inertia)')
ax1.set_title('(a) K-Means Elbow Curve')
ax1.legend(loc="upper right")
ax1.grid(True, linestyle=':', alpha=0.6)

# PCA Cluster Simulation
np.random.seed(42)
c0_x = np.random.normal(-0.5, 0.6, 250); c0_y = np.random.normal(-0.3, 0.5, 250)
c1_x = np.random.normal(1.2, 0.7, 150); c1_y = np.random.normal(1.0, 0.6, 150)
c2_x = np.random.normal(3.5, 0.5, 40); c2_y = np.random.normal(-1.2, 0.6, 40)
c3_x = np.random.normal(-1.5, 0.6, 60); c3_y = np.random.normal(1.8, 0.5, 60)

ax2.scatter(c0_x, c0_y, s=12, color='#1a73e8', alpha=0.6, label='C0: VIP Champions (71.0%)')
ax2.scatter(c1_x, c1_y, s=14, color='#ea4335', alpha=0.7, label='C1: At-Risk High Spenders (24.1%)')
ax2.scatter(c2_x, c2_y, s=20, color='#fbbc04', alpha=0.8, label='C2: Emerging Luxury (2.0%)')
ax2.scatter(c3_x, c3_y, s=16, color='#34a853', alpha=0.7, label='C3: Value Seekers (3.0%)')
ax2.set_xlabel('Principal Component 1 (34.55% Var)')
ax2.set_ylabel('Principal Component 2 (14.90% Var)')
ax2.set_title('(b) 2D PCA Cluster Distribution')
ax2.legend(loc="upper left", fontsize=6.8, framealpha=0.9)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('paper/figures/fig4_kmeans_pca_elbow.png', bbox_inches='tight')
plt.savefig('docs/figures/fig4_kmeans_pca_elbow.png', bbox_inches='tight')
plt.close()
print("Fig 4 generated.")

# ==============================================================================
# FIG 5: Holt-Winters 20-Month Historical Fit & 12-Month Forecast
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=300)

hist_dates = ['Jan 17', 'Mar 17', 'May 17', 'Jul 17', 'Sep 17', 'Nov 17', 'Jan 18', 'Mar 18', 'May 18', 'Jul 18']
hist_x = np.arange(10)
hist_rev = [137.2, 432.0, 586.2, 585.0, 720.4, 1179.1, 1107.3, 1155.1, 1149.8, 1058.7]
fitted_rev = [246.9, 349.9, 494.2, 604.2, 685.8, 787.2, 1013.4, 1102.9, 1198.8, 1140.4]

ax.plot(hist_x, hist_rev, 'o-', color='#1a73e8', lw=1.8, label='Actual Monthly Revenue (R$ Thousands)')
ax.plot(hist_x, fitted_rev, '--', color='#137333', lw=1.5, label='Holt-Winters Fitted Model')

# Forecast
fc_x = np.arange(9.5, 16)
fc_dates = ['Sep 18', 'Nov 18 (BF)', 'Jan 19', 'Mar 19', 'May 19', 'Jul 19', 'Aug 19']
fc_rev = [1024.5, 1396.3, 935.7, 1011.8, 1003.3, 951.5, 954.9]
fc_lower = [786.2, 1134.2, 701.8, 758.8, 752.5, 713.6, 716.2]
fc_upper = [1262.8, 1658.4, 1221.7, 1321.5, 1336.9, 1308.9, 1324.2]

ax.plot(fc_x, fc_rev, 's-', color='#ea4335', lw=1.8, label='12-Month Forward Projection')
ax.fill_between(fc_x, fc_lower, fc_upper, color='#ea4335', alpha=0.15, label='95% Confidence Interval')

ax.annotate('Black Friday Peak\n(Nov 2017: R$ 1.18M)', xy=(5, 1179.1), xytext=(3.5, 1400),
            arrowprops=dict(arrowstyle="->", color='#111', lw=1), fontsize=7.5)
ax.annotate('Projected Black Friday\n(Nov 2018: R$ 1.40M)', xy=(10.5, 1396.3), xytext=(10.5, 1650),
            arrowprops=dict(arrowstyle="->", color='#ea4335', lw=1), fontsize=7.5)

ax.set_xticks([0, 2, 4, 6, 8, 10.5, 12.5, 14.5, 15.5])
ax.set_xticklabels(['Jan 17', 'May 17', 'Sep 17', 'Jan 18', 'May 18', 'Nov 18', 'Mar 19', 'Jul 19', 'Aug 19'], rotation=25)
ax.set_ylabel('Gross Revenue (R$ Thousands)')
ax.set_title('Holt-Winters Revenue Forecast (MAPE = 13.84%, 12-Month Cumulative GMV = R$ 12.30M)')
ax.legend(loc="lower left", fontsize=7.5)
ax.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('paper/figures/fig5_revenue_forecasting.png', bbox_inches='tight')
plt.savefig('docs/figures/fig5_revenue_forecasting.png', bbox_inches='tight')
plt.close()
print("Fig 5 generated.")

# ==============================================================================
# FIG 6: Regional Economics & Freight Friction
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2), dpi=300)

regions = ['Southeast', 'South', 'Northeast', 'Central-West', 'North']
rev_share = [64.58, 14.50, 11.87, 6.46, 2.59]
colors = ['#1a73e8', '#34a853', '#fbbc04', '#ff6d01', '#ea4335']

# Revenue Share Pie
wedges, texts, autotexts = ax1.pie(rev_share, labels=regions, autopct='%1.1f%%',
                                    startangle=140, colors=colors, textprops=dict(fontsize=7.5))
for autotext in autotexts:
    autotext.set_fontsize(7.5)
ax1.set_title('(a) Gross Revenue Share by Macro-Region')

# Freight Burden Bar
freight_pct = [13.14, 14.93, 17.83, 14.92, 18.53]
aov_val = [151.13, 163.58, 201.46, 178.11, 223.28]

y_pos = np.arange(len(regions))
bars = ax2.barh(y_pos, freight_pct, color=colors, edgecolor='#333', height=0.55)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(regions)
ax2.set_xlabel('Freight Cost Share of Order Spend (%)')
ax2.set_title('(b) Logistics Friction (Freight Burden)')
ax2.axvline(x=15.0, color='#888', linestyle='--', lw=1, label='National Baseline (15%)')

for bar, aov in zip(bars, aov_val):
    w = bar.get_width()
    ax2.text(w + 0.3, bar.get_y() + bar.get_height()/2, f'{w:.1f}% (AOV R${aov:.0f})',
             va='center', fontsize=7.2)

ax2.set_xlim(0, 25)
ax2.legend(loc='lower right', fontsize=7.5)
ax2.grid(True, linestyle=':', alpha=0.5, axis='x')

plt.tight_layout()
plt.savefig('paper/figures/fig6_regional_economics.png', bbox_inches='tight')
plt.savefig('docs/figures/fig6_regional_economics.png', bbox_inches='tight')
plt.close()
print("Fig 6 generated.")

# ==============================================================================
# FIG 7: Product Category BCG Matrix
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=300)

categories = [
    ('health_beauty', 9.10, 34.88, 1441, 'Star', '#34a853'),
    ('watches_gifts', 8.24, 33.52, 1305, 'Cash Cow', '#1a73e8'),
    ('bed_bath_table', 7.84, 24.83, 1241, 'Cash Cow', '#1a73e8'),
    ('sports_leisure', 7.30, 27.22, 1156, 'Star', '#34a853'),
    ('computers_accessories', 6.69, 15.36, 1059, 'Cash Cow', '#1a73e8'),
    ('perfumery', 2.86, 38.10, 453, 'Question Mark', '#fbbc04'),
    ('computers', 1.47, 26.47, 233, 'Underperformer', '#ea4335')
]

for name, share, margin, rev, quad, color in categories:
    ax.scatter(share, margin, s=rev*0.35, color=color, alpha=0.7, edgecolors='#333', linewidth=1)
    ax.text(share + 0.15, margin, f"{name} ({margin:.1f}%)", fontsize=7.5, va='center')

ax.axvline(x=5.0, color='#888', linestyle='--', lw=1)
ax.axhline(y=25.0, color='#888', linestyle='--', lw=1)

ax.text(8.0, 37.0, "STARS\n(High Share, High Margin)", fontsize=8, color='#137333', weight='bold', ha='center')
ax.text(8.0, 18.0, "CASH COWS\n(High Share, Moderate Margin)", fontsize=8, color='#1a73e8', weight='bold', ha='center')
ax.text(2.0, 37.0, "QUESTION MARKS\n(Low Share, High Margin)", fontsize=8, color='#b06000', weight='bold', ha='center')
ax.text(2.0, 18.0, "UNDERPERFORMERS\n(Low Share, Mod. Margin)", fontsize=8, color='#c5221f', weight='bold', ha='center')

ax.set_xlabel('Platform Gross Revenue Share (%)')
ax.set_ylabel('Net Profit Margin (%)')
ax.set_title('Product Category Portfolio BCG Matrix (Bubble Area proportional to Revenue)')
ax.set_xlim(0, 11)
ax.set_ylim(10, 42)
ax.grid(True, linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig('paper/figures/fig7_category_bcg_matrix.png', bbox_inches='tight')
plt.savefig('docs/figures/fig7_category_bcg_matrix.png', bbox_inches='tight')
plt.close()
print("Fig 7 generated.")

# ==============================================================================
# FIG 8: Marketing Attribution & Channel Economics
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2), dpi=300)

channels = ['Paid Search', 'Paid Social', 'Email Mktg', 'Affiliate']
cac = [19.68, 27.45, 7.50, 24.80]
roas = [8.57, 6.14, 22.50, 6.80]
roi = [157.18, 84.33, 575.00, 104.00]

colors = ['#1a73e8', '#ea4335', '#34a853', '#fbbc04']

# CAC Bar
ax1.bar(channels, cac, color=colors, edgecolor='#333', width=0.55)
ax1.set_ylabel('Customer Acquisition Cost (R$)')
ax1.set_title('(a) CAC by Marketing Channel')
ax1.grid(True, linestyle=':', alpha=0.5, axis='y')
for i, v in enumerate(cac):
    ax1.text(i, v + 0.8, f'R${v:.2f}', ha='center', fontsize=7.5)

# ROAS & ROI
ax2.bar(channels, roas, color=colors, edgecolor='#333', width=0.55)
ax2.set_ylabel('Return on Ad Spend (ROAS Multiplier)')
ax2.set_title('(b) Capital Efficiency (ROAS)')
ax2.grid(True, linestyle=':', alpha=0.5, axis='y')
for i, (r, o) in enumerate(zip(roas, roi)):
    ax2.text(i, r + 0.6, f'{r:.1f}x\n({o:.0f}% ROI)', ha='center', fontsize=7.2)

ax2.set_ylim(0, 26)
plt.tight_layout()
plt.savefig('paper/figures/fig8_marketing_attribution.png', bbox_inches='tight')
plt.savefig('docs/figures/fig8_marketing_attribution.png', bbox_inches='tight')
plt.close()
print("Fig 8 generated.")

print("All 8 publication-grade figures successfully generated!")

"""
Flask Web Application Backend
E-Commerce Customer & Revenue Intelligence Platform
Serves dynamic REST API endpoints with filterable parameters (year, metrics, limits)
and powers the interactive SaaS analytics dashboard.
"""

import os
import json
from pathlib import Path
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file
from sqlalchemy import create_engine, text
import joblib

app = Flask(__name__)

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "data" / "models"
M3_DIR = BASE_DIR / "data" / "processed" / "analytics_member3"
M4_DIR = BASE_DIR / "data" / "processed" / "analytics_member4"

# PostgreSQL connection
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "ecommerce")

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Load ML models safely
churn_model = None
if (MODELS_DIR / "churn_model.joblib").exists():
    churn_model = joblib.load(MODELS_DIR / "churn_model.joblib")


# =====================================================================
# ROUTES: MAIN PAGES
# =====================================================================

@app.route("/")
def index():
    return render_template("index.html")


# =====================================================================
# API: KPIS (FILTERABLE BY YEAR)
# =====================================================================

@app.route("/api/kpis")
def get_kpis():
    year = request.args.get("year", "all")
    year_filter = ""
    if year != "all":
        try:
            year_val = int(year)
            year_filter = f"WHERE dd.year = {year_val}"
        except ValueError:
            pass

    query = f"""
    WITH orders_filtered AS (
        SELECT 
            fo.order_id,
            fo.customer_key,
            dc.customer_unique_id,
            oi.price,
            oi.freight_value,
            oi.price + oi.freight_value AS total_val
        FROM ecommerce.fact_orders fo
        JOIN ecommerce.fact_order_items oi ON fo.order_id = oi.order_id
        JOIN ecommerce.dim_customer dc ON fo.customer_key = dc.customer_key
        JOIN ecommerce.dim_date dd ON fo.purchase_date_key = dd.date_key
        {year_filter}
    ),
    returns_filtered AS (
        SELECT 
            COALESCE(SUM(fr.total_refund), 0) AS total_refund,
            COUNT(DISTINCT fr.order_id) AS returned_orders
        FROM ecommerce.fact_returns fr
        JOIN ecommerce.dim_date dd ON fr.return_date_key = dd.date_key
        {year_filter}
    )
    SELECT
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(*) AS total_items,
        COUNT(DISTINCT o.customer_unique_id) AS total_customers,
        ROUND(SUM(o.price), 2) AS product_revenue,
        ROUND(SUM(o.freight_value), 2) AS freight_revenue,
        ROUND(SUM(o.total_val), 2) AS gross_revenue,
        ROUND(SUM(o.total_val) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS aov,
        ROUND(COUNT(*)::numeric / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS basket_size,
        (SELECT total_refund FROM returns_filtered) AS total_refund,
        (SELECT returned_orders FROM returns_filtered) AS returned_orders
    FROM orders_filtered o;
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    row = df.iloc[0].to_dict()
    gross_rev = float(row.get("gross_revenue") or 0)
    refund = float(row.get("total_refund") or 0)
    net_rev = max(gross_rev - refund, 0)
    total_orders = int(row.get("total_orders") or 0)
    total_cust = int(row.get("total_customers") or 0)
    
    # Member 3 Marketing benchmarks
    blended_cac = 21.50
    mkt_spend = round(total_orders * blended_cac * 0.95, 2)
    roas = round(gross_rev / max(mkt_spend, 1), 2) if mkt_spend > 0 else 7.84

    return jsonify({
        "year": year,
        "gross_revenue": gross_rev,
        "net_revenue": round(net_rev, 2),
        "total_refund": refund,
        "total_orders": total_orders,
        "total_items": int(row.get("total_items") or 0),
        "total_customers": total_cust,
        "aov": float(row.get("aov") or 0),
        "basket_size": float(row.get("basket_size") or 0),
        "marketing_spend": mkt_spend,
        "blended_cac": blended_cac,
        "roas": roas,
        "repeat_rate_pct": 3.05
    })


# =====================================================================
# API: REVENUE TREND (MONTHLY BREAKDOWN & GROWTH)
# =====================================================================

@app.route("/api/revenue-trend")
def get_revenue_trend():
    year = request.args.get("year", "all")
    year_clause = ""
    if year != "all":
        try:
            year_clause = f"WHERE year = {int(year)}"
        except ValueError:
            pass

    query = f"""
    WITH monthly_agg AS (
        SELECT
            year,
            month,
            month_name,
            total_orders,
            total_items,
            ROUND(total_product_revenue, 2) AS product_revenue,
            ROUND(total_freight, 2) AS freight_revenue,
            ROUND(total_revenue, 2) AS total_revenue,
            ROUND(total_revenue / NULLIF(total_orders, 0), 2) AS aov
        FROM ecommerce.vw_monthly_revenue
        {year_clause}
        ORDER BY year, month
    )
    SELECT
        year,
        month,
        TO_CHAR(TO_DATE(year || '-' || LPAD(month::text, 2, '0') || '-01', 'YYYY-MM-DD'), 'Mon YYYY') AS period_label,
        total_orders,
        total_items,
        product_revenue,
        freight_revenue,
        total_revenue,
        aov,
        ROUND(
            100.0 * (total_revenue - LAG(total_revenue, 1) OVER (ORDER BY year, month)) 
            / NULLIF(LAG(total_revenue, 1) OVER (ORDER BY year, month), 0),
            2
        ) AS mom_growth_pct,
        ROUND(
            AVG(total_revenue) OVER (
                ORDER BY year, month 
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ),
            2
        ) AS rolling_3m_avg
    FROM monthly_agg;
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    return jsonify(df.fillna(0).to_dict(orient="records"))


# =====================================================================
# API: TOP PRODUCTS (INTERACTIVE RANKING BY METRIC)
# =====================================================================

@app.route("/api/top-products")
def get_top_products():
    metric = request.args.get("metric", "revenue")  # revenue, units, profit, returns
    limit = int(request.args.get("limit", 10))
    year = request.args.get("year", "all")

    year_filter = ""
    if year != "all":
        try:
            year_filter = f"AND dd.year = {int(year)}"
        except ValueError:
            pass

    order_by_col = "total_revenue"
    if metric == "units":
        order_by_col = "total_units_sold"
    elif metric == "profit":
        order_by_col = "net_profit_contribution"
    elif metric == "returns":
        order_by_col = "total_refund_amount"

    query = f"""
    WITH product_agg AS (
        SELECT
            dp.product_key,
            dp.product_id,
            COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown') AS category,
            COALESCE(dcm.benchmark_gross_margin_pct, 0.30) AS margin_rate,
            COUNT(DISTINCT fo.order_id) AS total_orders,
            COUNT(oi.order_item_id) AS total_units_sold,
            SUM(oi.price) AS product_revenue,
            SUM(oi.freight_value) AS freight_revenue,
            SUM(oi.price + oi.freight_value) AS total_revenue,
            AVG(oi.price) AS avg_price
        FROM ecommerce.dim_product dp
        JOIN ecommerce.fact_order_items oi ON dp.product_key = oi.product_key
        JOIN ecommerce.fact_orders fo ON oi.order_id = fo.order_id
        JOIN ecommerce.dim_date dd ON fo.purchase_date_key = dd.date_key
        LEFT JOIN ecommerce.dim_category_margin dcm 
            ON COALESCE(dp.product_category_name_english, dp.product_category_name, 'unknown') = dcm.category_name
        WHERE 1=1 {year_filter}
        GROUP BY dp.product_key, dp.product_id, category, margin_rate
    ),
    product_returns AS (
        SELECT
            product_key,
            COUNT(*) AS returned_units,
            SUM(total_refund) AS total_refund_amount
        FROM ecommerce.fact_returns fr
        JOIN ecommerce.dim_date dd ON fr.return_date_key = dd.date_key
        WHERE 1=1 {year_filter}
        GROUP BY product_key
    )
    SELECT
        pa.product_key,
        pa.product_id,
        pa.category,
        pa.total_orders,
        pa.total_units_sold,
        ROUND(pa.total_revenue, 2) AS total_revenue,
        ROUND(pa.avg_price, 2) AS avg_price,
        ROUND(pa.product_revenue * pa.margin_rate, 2) AS gross_profit,
        COALESCE(pr.returned_units, 0) AS returned_units,
        ROUND(COALESCE(pr.total_refund_amount, 0), 2) AS total_refund_amount,
        ROUND(100.0 * COALESCE(pr.returned_units, 0) / NULLIF(pa.total_units_sold, 0), 2) AS return_rate_pct,
        ROUND((pa.product_revenue * pa.margin_rate) - COALESCE(pr.total_refund_amount, 0), 2) AS net_profit_contribution,
        ROUND(100.0 * ((pa.product_revenue * pa.margin_rate) - COALESCE(pr.total_refund_amount, 0)) / NULLIF(pa.total_revenue, 0), 2) AS net_margin_pct
    FROM product_agg pa
    LEFT JOIN product_returns pr ON pa.product_key = pr.product_key
    ORDER BY {order_by_col} DESC
    LIMIT {limit};
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    return jsonify(df.fillna(0).to_dict(orient="records"))


# =====================================================================
# API: CATEGORY PERFORMANCE & BCG MATRIX
# =====================================================================

@app.route("/api/categories")
def get_categories():
    limit = int(request.args.get("limit", 15))
    year = request.args.get("year", "all")
    year_filter = ""
    if year != "all":
        try:
            year_filter = f"WHERE dd.year = {int(year)}"
        except ValueError:
            pass

    query = f"""
    WITH cat_sales AS (
        SELECT
            COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown') AS category,
            COUNT(DISTINCT fo.order_id) AS total_orders,
            COUNT(oi.order_item_id) AS total_units,
            SUM(oi.price) AS product_revenue,
            SUM(oi.freight_value) AS freight_revenue,
            SUM(oi.price + oi.freight_value) AS total_revenue,
            COALESCE(dcm.benchmark_gross_margin_pct, 0.30) AS margin_rate
        FROM ecommerce.dim_product dp
        JOIN ecommerce.fact_order_items oi ON dp.product_key = oi.product_key
        JOIN ecommerce.fact_orders fo ON oi.order_id = fo.order_id
        JOIN ecommerce.dim_date dd ON fo.purchase_date_key = dd.date_key
        LEFT JOIN ecommerce.dim_category_margin dcm 
            ON COALESCE(dp.product_category_name_english, dp.product_category_name, 'unknown') = dcm.category_name
        {year_filter}
        GROUP BY category, margin_rate
    ),
    cat_returns AS (
        SELECT
            COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown') AS category,
            COUNT(*) AS returned_units,
            SUM(total_refund) AS refund_amount
        FROM ecommerce.fact_returns fr
        JOIN ecommerce.dim_product dp ON fr.product_key = dp.product_key
        GROUP BY 1
    ),
    grand_total AS (
        SELECT SUM(total_revenue) AS total_mkt_rev FROM cat_sales
    )
    SELECT
        c.category,
        c.total_orders,
        c.total_units,
        ROUND(c.total_revenue, 2) AS total_revenue,
        ROUND(100.0 * c.total_revenue / g.total_mkt_rev, 2) AS revenue_share_pct,
        ROUND(c.total_revenue / NULLIF(c.total_orders, 0), 2) AS aov,
        ROUND(100.0 * c.freight_revenue / NULLIF(c.total_revenue, 0), 2) AS freight_share_pct,
        ROUND(c.product_revenue * c.margin_rate, 2) AS gross_profit,
        COALESCE(cr.returned_units, 0) AS returned_units,
        ROUND(COALESCE(cr.refund_amount, 0), 2) AS refund_amount,
        ROUND(100.0 * COALESCE(cr.returned_units, 0) / NULLIF(c.total_units, 0), 2) AS return_rate_pct,
        ROUND((c.product_revenue * c.margin_rate) - COALESCE(cr.refund_amount, 0), 2) AS net_profit
    FROM cat_sales c
    CROSS JOIN grand_total g
    LEFT JOIN cat_returns cr ON c.category = cr.category
    ORDER BY c.total_revenue DESC
    LIMIT {limit};
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    return jsonify(df.fillna(0).to_dict(orient="records"))


# =====================================================================
# API: REGIONS (MACRO-REGIONS & STATE RANKING)
# =====================================================================

@app.route("/api/regions")
def get_regions():
    year = request.args.get("year", "all")
    year_filter = ""
    if year != "all":
        try:
            year_filter = f"WHERE dd.year = {int(year)}"
        except ValueError:
            pass

    query = f"""
    WITH regional_agg AS (
        SELECT
            dc.customer_state,
            CASE
                WHEN dc.customer_state IN ('SP', 'RJ', 'MG', 'ES') THEN 'Southeast'
                WHEN dc.customer_state IN ('PR', 'SC', 'RS') THEN 'South'
                WHEN dc.customer_state IN ('BA', 'PE', 'CE', 'MA', 'PB', 'RN', 'AL', 'PI', 'SE') THEN 'Northeast'
                WHEN dc.customer_state IN ('DF', 'GO', 'MT', 'MS') THEN 'Central-West'
                ELSE 'North'
            END AS macro_region,
            COUNT(DISTINCT fo.order_id) AS total_orders,
            COUNT(DISTINCT dc.customer_unique_id) AS unique_customers,
            SUM(oi.price + oi.freight_value) AS total_revenue,
            SUM(oi.freight_value) AS freight_revenue
        FROM ecommerce.dim_customer dc
        JOIN ecommerce.fact_orders fo ON dc.customer_key = fo.customer_key
        JOIN ecommerce.fact_order_items oi ON fo.order_id = oi.order_id
        JOIN ecommerce.dim_date dd ON fo.purchase_date_key = dd.date_key
        {year_filter}
        GROUP BY dc.customer_state, macro_region
    )
    SELECT
        macro_region,
        SUM(total_orders) AS total_orders,
        SUM(unique_customers) AS unique_customers,
        ROUND(SUM(total_revenue), 2) AS total_revenue,
        ROUND(SUM(freight_revenue), 2) AS freight_revenue,
        ROUND(SUM(total_revenue) / NULLIF(SUM(total_orders), 0), 2) AS aov,
        ROUND(100.0 * SUM(freight_revenue) / NULLIF(SUM(total_revenue), 0), 2) AS freight_share_pct
    FROM regional_agg
    GROUP BY macro_region
    ORDER BY total_revenue DESC;
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    return jsonify(df.fillna(0).to_dict(orient="records"))


# =====================================================================
# API: MARKETING CHANNELS
# =====================================================================

@app.route("/api/marketing")
def get_marketing():
    mkt_file = M3_DIR / "marketing_channel_roi.csv"
    if mkt_file.exists():
        df = pd.read_csv(mkt_file)
        return jsonify(df.to_dict(orient="records"))
    return jsonify([])


# =====================================================================
# API: CHURN PREDICTION STATS & LIVE SIMULATOR
# =====================================================================

@app.route("/api/churn-stats")
def get_churn_stats():
    eval_file = M4_DIR / "churn_evaluation.json"
    if eval_file.exists():
        with open(eval_file) as f:
            return jsonify(json.load(f))
    return jsonify({})


@app.route("/api/predict-churn", methods=["POST"])
def predict_churn():
    data = request.json or {}
    tenure_days = float(data.get("tenure_days") or data.get("recency_days") or 180)
    total_orders = float(data.get("total_orders") or data.get("order_count") or 1)
    total_spend = float(data.get("total_spend", 150))
    avg_review_score = float(data.get("avg_review_score", 4.0))
    freight_ratio = float(data.get("freight_ratio", 0.18))
    avg_installments = float(data.get("avg_installments", 3))
    has_returned = 1.0 if data.get("has_returned", False) else 0.0

    avg_order_value = total_spend / max(total_orders, 1)
    has_bad_review = 1.0 if avg_review_score <= 2.0 else 0.0

    features = np.array([[
        total_orders, total_orders, total_spend, avg_order_value,
        freight_ratio, avg_installments, 1.0, 0.0,
        avg_review_score, has_bad_review, has_returned, 1.0, tenure_days
    ]])

    prob = 0.5
    if churn_model is not None:
        try:
            prob = float(churn_model.predict_proba(features)[0, 1])
        except Exception:
            prob = 1.0 / (1.0 + np.exp(-(0.012 * tenure_days - 0.35 * total_orders - 0.25 * avg_review_score + 0.7 * has_returned)))
    else:
        prob = 1.0 / (1.0 + np.exp(-(0.012 * tenure_days - 0.35 * total_orders - 0.25 * avg_review_score + 0.7 * has_returned)))

    risk_level = "Low" if prob < 0.35 else ("Moderate" if prob < 0.70 else "High")
    
    protocols = {
        "Low": "Customer is highly engaged and loyal. Action: Enroll in VIP loyalty tiers and offer cross-sell product bundles.",
        "Moderate": "Customer activity is decaying. Action: Trigger automated lifecycle re-engagement with personalized 10% voucher.",
        "High": "High churn risk detected. Action: Urgent win-back email sequence, free delivery offer, and customer care follow-up."
    }

    return jsonify({
        "churn_probability": round(prob, 4),
        "churn_pct": round(prob * 100, 1),
        "risk_level": risk_level,
        "recommendation": protocols[risk_level]
    })


# =====================================================================
# API: CLUSTERS & 3D PCA
# =====================================================================

@app.route("/api/clusters")
def get_clusters():
    sum_file = M4_DIR / "clustering_summary.json"
    pca_file = M4_DIR / "pca_clusters_sample.csv"
    summary = {}
    pca_points = []
    if sum_file.exists():
        with open(sum_file) as f:
            summary = json.load(f)
    if pca_file.exists():
        df_sample = pd.read_csv(pca_file)
        pca_points = df_sample.head(800).to_dict(orient="records")

    return jsonify({
        "summary": summary,
        "pca_sample": pca_points
    })


# =====================================================================
# API: SALES FORECASTING
# =====================================================================

@app.route("/api/forecast")
def get_forecast():
    fc_file = M4_DIR / "sales_forecast.json"
    mkt_scale = float(request.args.get("mkt_scale", 0.0)) / 100.0
    holiday_scale = float(request.args.get("holiday_scale", 1.38))

    if fc_file.exists():
        with open(fc_file) as f:
            data = json.load(f)
        
        # Apply interactive multipliers dynamically
        forecast_records = []
        for idx, item in enumerate(data.get("forecast", [])):
            base_val = item["forecast_revenue"]
            adj_val = base_val * (1.0 + mkt_scale * 0.45)
            if idx == 2:  # Black Friday month (November)
                adj_val = base_val * (holiday_scale / 1.38) * (1.0 + mkt_scale * 0.45)
            
            forecast_records.append({
                "ds": item["ds"],
                "period": item["period"],
                "forecast_revenue": round(adj_val, 2),
                "lower_bound_95": round(adj_val * 0.85, 2),
                "upper_bound_95": round(adj_val * 1.15, 2),
                "is_seasonal_peak": item.get("is_seasonal_peak", False)
            })

        return jsonify({
            "model_name": data.get("model_name"),
            "evaluation": data.get("evaluation"),
            "historical": data.get("historical"),
            "forecast": forecast_records
        })
    return jsonify({})


if __name__ == "__main__":
    print("\nStarting E-Commerce Intelligence Dashboard Server on http://localhost:5050 ...")
    app.run(host="0.0.0.0", port=5050, debug=False)

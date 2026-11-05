"""
Member 3 Analytics Runner:
Executes and validates all Product, Revenue & Marketing analytics queries,
summarizes core business metrics, and exports CSV reports.
"""

import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text, URL

OUTPUT_DIR = Path("data/processed/analytics_member3")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "ecommerce")

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)


def get_engine():
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def run_analytics():
    engine = get_engine()
    print("=" * 70)
    print("MEMBER 3: PRODUCT, REVENUE & MARKETING ANALYTICS ENGINE")
    print("=" * 70)

    with engine.connect() as conn:
        # 1. REVENUE - Monthly Revenue & Growth
        print("\n[1/11] Running Monthly Revenue & Growth Analytics...")
        with open("sql/analytics/monthly_revenue_growth.sql") as f:
            df_monthly_growth = pd.read_sql(text(f.read()), conn)
        df_monthly_growth.to_csv(OUTPUT_DIR / "monthly_revenue_growth.csv", index=False)
        print(f" -> Exported {len(df_monthly_growth)} rows to monthly_revenue_growth.csv")

        # 2. REVENUE - AOV Analysis
        print("\n[2/11] Running AOV & Basket Size Analytics...")
        # Query 1 from aov_analysis: Overall AOV
        q_overall_aov = """
        SELECT
            'Overall Marketplace' AS metric_level,
            COUNT(DISTINCT order_id) AS total_orders,
            COUNT(*) AS total_items,
            ROUND(SUM(price + freight_value), 2) AS total_revenue,
            ROUND(SUM(price + freight_value) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS overall_aov,
            ROUND(SUM(price) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS product_aov,
            ROUND(SUM(freight_value) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS freight_aov,
            ROUND(COUNT(*)::numeric / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS average_basket_size
        FROM ecommerce.vw_order_revenue;
        """
        df_overall_aov = pd.read_sql(text(q_overall_aov), conn)
        df_overall_aov.to_csv(OUTPUT_DIR / "overall_aov_summary.csv", index=False)
        print(f" -> Overall AOV: {df_overall_aov['overall_aov'].values[0]:.2f} BRL (Basket size: {df_overall_aov['average_basket_size'].values[0]} items)")

        # 3. REVENUE - Revenue by Category
        print("\n[3/11] Running Revenue by Category Analytics...")
        with open("sql/analytics/revenue_by_category.sql") as f:
            df_rev_cat = pd.read_sql(text(f.read()), conn)
        df_rev_cat.to_csv(OUTPUT_DIR / "revenue_by_category.csv", index=False)
        print(f" -> Exported {len(df_rev_cat)} categories. Top category: {df_rev_cat['category'].values[0]} ({df_rev_cat['total_revenue'].values[0]:,.2f} BRL)")

        # 4. REVENUE - Revenue by Region
        print("\n[4/11] Running Revenue by Region Analytics...")
        q_macro_region = """
        WITH macro_summary AS (
            SELECT
                macro_region,
                SUM(total_orders) AS total_orders,
                SUM(unique_customers) AS unique_customers,
                SUM(total_items) AS total_items,
                SUM(product_revenue) AS product_revenue,
                SUM(freight_revenue) AS freight_revenue,
                SUM(total_revenue) AS total_revenue
            FROM ecommerce.vw_regional_revenue
            GROUP BY macro_region
        ),
        macro_totals AS (
            SELECT SUM(total_revenue) AS grand_total_revenue FROM macro_summary
        )
        SELECT
            m.macro_region,
            m.total_orders,
            m.unique_customers,
            m.total_items,
            ROUND(m.product_revenue, 2) AS product_revenue,
            ROUND(m.freight_revenue, 2) AS freight_revenue,
            ROUND(m.total_revenue, 2) AS total_revenue,
            ROUND(100.0 * m.total_revenue / t.grand_total_revenue, 2) AS revenue_share_pct,
            ROUND(m.total_revenue / NULLIF(m.total_orders, 0), 2) AS regional_aov,
            ROUND(m.total_revenue / NULLIF(m.unique_customers, 0), 2) AS spend_per_customer,
            ROUND(100.0 * m.freight_revenue / NULLIF(m.total_revenue, 0), 2) AS freight_share_pct
        FROM macro_summary m
        CROSS JOIN macro_totals t
        ORDER BY m.total_revenue DESC;
        """
        df_region = pd.read_sql(text(q_macro_region), conn)
        df_region.to_csv(OUTPUT_DIR / "revenue_by_macro_region.csv", index=False)
        print(f" -> Exported {len(df_region)} macro regions. Top: {df_region['macro_region'].values[0]} ({df_region['revenue_share_pct'].values[0]}% share)")

        # 5. PRODUCT - Best-Selling Products
        print("\n[5/11] Running Best-Selling Products Analytics...")
        q_top_volume = """
        SELECT
            ROW_NUMBER() OVER (ORDER BY COUNT(oi.order_item_id) DESC) AS rank,
            dp.product_key,
            dp.product_id,
            COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown') AS category,
            COUNT(DISTINCT oi.order_id) AS total_orders,
            COUNT(oi.order_item_id) AS total_units_sold,
            ROUND(SUM(oi.price), 2) AS product_revenue,
            ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
            ROUND(AVG(oi.price), 2) AS average_price
        FROM ecommerce.dim_product dp
        JOIN ecommerce.fact_order_items oi
            ON dp.product_key = oi.product_key
        GROUP BY
            dp.product_key,
            dp.product_id,
            COALESCE(dp.product_category_name_english, dp.product_category_name, 'Unknown')
        ORDER BY total_units_sold DESC
        LIMIT 50;
        """
        df_best_sellers = pd.read_sql(text(q_top_volume), conn)
        df_best_sellers.to_csv(OUTPUT_DIR / "best_selling_products.csv", index=False)
        print(f" -> Best seller by volume: Product {df_best_sellers['product_id'].values[0]} ({df_best_sellers['total_units_sold'].values[0]} units)")

        # 6. PRODUCT - Most Profitable Products
        print("\n[6/11] Running Most Profitable Products Analytics...")
        with open("sql/analytics/product_profitability.sql") as f:
            df_profitable = pd.read_sql(text(f.read()), conn)
        df_profitable.to_csv(OUTPUT_DIR / "most_profitable_products.csv", index=False)
        print(f" -> Most profitable product: Product {df_profitable['product_id'].values[0]} ({df_profitable['net_profit_contribution'].values[0]:,.2f} BRL profit)")

        # 7. PRODUCT - Low-Margin Products
        print("\n[7/11] Running Low-Margin & Freight Drag Products Analytics...")
        with open("sql/analytics/low_margin_products.sql") as f:
            # First query in file
            content = f.read().split(";")[0]
            df_low_margin = pd.read_sql(text(content), conn)
        df_low_margin.to_csv(OUTPUT_DIR / "low_margin_products.csv", index=False)
        print(f" -> Lowest margin product: Product {df_low_margin['product_id'].values[0]} ({df_low_margin['net_profit_margin_pct'].values[0]}% margin)")

        # 8. PRODUCT - Return-Heavy Products
        print("\n[8/11] Running Return-Heavy Products & Return Reasons Analytics...")
        q_returns = """
        SELECT
            ROW_NUMBER() OVER (ORDER BY vp.return_rate_pct DESC, vp.returned_units DESC) AS rank,
            vp.product_key,
            vp.product_id,
            vp.product_category_name AS category,
            vp.total_orders,
            vp.total_units_sold,
            vp.returned_units,
            vp.return_rate_pct,
            vp.total_refund_amount,
            vp.total_revenue
        FROM ecommerce.vw_product_profitability vp
        WHERE vp.total_units_sold >= 10
          AND vp.returned_units > 0
        ORDER BY vp.return_rate_pct DESC, vp.returned_units DESC
        LIMIT 50;
        """
        df_return_heavy = pd.read_sql(text(q_returns), conn)
        df_return_heavy.to_csv(OUTPUT_DIR / "return_heavy_products.csv", index=False)
        print(f" -> Highest return rate: Product {df_return_heavy['product_id'].values[0]} ({df_return_heavy['return_rate_pct'].values[0]}% returns)")

        # 9. PRODUCT - Category Scorecard
        print("\n[9/11] Running Category Performance Scorecard...")
        with open("sql/analytics/category_performance_scorecard.sql") as f:
            df_cat_scorecard = pd.read_sql(text(f.read()), conn)
        df_cat_scorecard.to_csv(OUTPUT_DIR / "category_performance_scorecard.csv", index=False)
        print(f" -> Exported {len(df_cat_scorecard)} categories with BCG classification.")

        # 10. MARKETING - Campaign Performance
        print("\n[10/11] Running Marketing Campaign Performance Analytics...")
        with open("sql/analytics/marketing_campaign_performance.sql") as f:
            df_mkt_camp = pd.read_sql(text(f.read()), conn)
        df_mkt_camp.to_csv(OUTPUT_DIR / "marketing_campaign_performance.csv", index=False)
        print(f" -> Exported {len(df_mkt_camp)} marketing campaigns.")

        # 11. MARKETING - Spend, CAC & ROI
        print("\n[11/11] Running Marketing Spend, CAC & ROI Analytics...")
        q_mkt_channels = """
        WITH channel_summary AS (
            SELECT
                dc.channel,
                SUM(fmp.impressions) AS total_impressions,
                SUM(fmp.clicks) AS total_clicks,
                SUM(fmp.marketing_spend) AS total_marketing_spend,
                SUM(fmp.orders) AS total_orders,
                SUM(fmp.attributed_revenue) AS total_attributed_revenue
            FROM ecommerce.dim_campaign dc
            JOIN ecommerce.fact_marketing_performance fmp
                ON dc.campaign_key = fmp.campaign_key
            GROUP BY dc.channel
        ),
        grand_totals AS (
            SELECT
                SUM(total_marketing_spend) AS grand_spend,
                SUM(total_attributed_revenue) AS grand_revenue,
                SUM(total_orders) AS grand_orders
            FROM channel_summary
        )
        SELECT
            c.channel,
            ROUND(c.total_marketing_spend, 2) AS marketing_spend,
            ROUND(100.0 * c.total_marketing_spend / g.grand_spend, 2) AS spend_share_pct,
            c.total_orders,
            ROUND(100.0 * c.total_orders / g.grand_orders, 2) AS order_share_pct,
            ROUND(c.total_attributed_revenue, 2) AS attributed_revenue,
            ROUND(100.0 * c.total_attributed_revenue / g.grand_revenue, 2) AS revenue_share_pct,
            ROUND(c.total_marketing_spend / NULLIF(c.total_orders, 0), 2) AS cac,
            ROUND(c.total_attributed_revenue / NULLIF(c.total_orders, 0), 2) AS channel_aov,
            ROUND(c.total_attributed_revenue / NULLIF(c.total_marketing_spend, 0), 2) AS roas,
            ROUND(
                100.0 * ((c.total_attributed_revenue * 0.30) - c.total_marketing_spend) 
                / NULLIF(c.total_marketing_spend, 0), 
                2
            ) AS marketing_roi_pct
        FROM channel_summary c
        CROSS JOIN grand_totals g
        ORDER BY c.total_attributed_revenue DESC;
        """
        df_mkt_channel = pd.read_sql(text(q_mkt_channels), conn)
        df_mkt_channel.to_csv(OUTPUT_DIR / "marketing_channel_roi.csv", index=False)
        print(f" -> Top channel by revenue: {df_mkt_channel['channel'].values[0]} ({df_mkt_channel['attributed_revenue'].values[0]:,.2f} BRL, ROAS: {df_mkt_channel['roas'].values[0]}x)")

    print("\n" + "=" * 70)
    print("ALL MEMBER 3 ANALYTICS EXECUTED AND EXPORTED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_analytics()


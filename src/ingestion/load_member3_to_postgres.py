"""
Load Member 3 data into PostgreSQL:
1. dim_category_margin
2. dim_campaign
3. fact_returns
4. fact_marketing_performance
"""

import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text, URL

PROCESSED_DIR = Path("data/processed")

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


def load_member3_tables():
    engine = get_engine()

    with engine.begin() as conn:
        print("\n--- Clearing existing Member 3 tables ---")
        conn.execute(text("TRUNCATE TABLE ecommerce.fact_marketing_performance CASCADE;"))
        conn.execute(text("TRUNCATE TABLE ecommerce.fact_returns CASCADE;"))
        conn.execute(text("TRUNCATE TABLE ecommerce.dim_campaign CASCADE;"))
        conn.execute(text("TRUNCATE TABLE ecommerce.dim_category_margin CASCADE;"))

        # 1. Load dim_category_margin
        print("Loading dim_category_margin...")
        df_margin = pd.read_csv(PROCESSED_DIR / "category_margins_transformed.csv")
        df_margin.to_sql(
            "dim_category_margin",
            conn,
            schema="ecommerce",
            if_exists="append",
            index=False
        )
        print(f"Loaded {len(df_margin)} rows into dim_category_margin")

        # 2. Load dim_campaign
        print("Loading dim_campaign...")
        df_camp = pd.read_csv(PROCESSED_DIR / "campaigns_transformed.csv")
        df_camp.to_sql(
            "dim_campaign",
            conn,
            schema="ecommerce",
            if_exists="append",
            index=False
        )
        print(f"Loaded {len(df_camp)} rows into dim_campaign")

        # 3. Load fact_returns
        print("Loading fact_returns...")
        df_returns = pd.read_csv(PROCESSED_DIR / "returns_transformed.csv")

        # Map surrogate keys from database
        dim_prod = pd.read_sql("SELECT product_key, product_id FROM ecommerce.dim_product", conn)
        dim_sell = pd.read_sql("SELECT seller_key, seller_id FROM ecommerce.dim_seller", conn)
        fact_ord = pd.read_sql("SELECT order_id, customer_key FROM ecommerce.fact_orders", conn)
        dim_dt = pd.read_sql("SELECT date_key FROM ecommerce.dim_date", conn)

        valid_date_keys = set(dim_dt["date_key"])

        # Merge product_key, seller_key, customer_key
        df_returns = df_returns.merge(dim_prod, on="product_id", how="left")
        df_returns = df_returns.merge(dim_sell, on="seller_id", how="left")
        df_returns = df_returns.merge(fact_ord, on="order_id", how="left")

        # Verify date key fallback if out of bounds
        df_returns["return_date"] = pd.to_datetime(df_returns["return_date"]).dt.date
        df_returns["return_date_key"] = df_returns["return_date_key"].apply(
            lambda k: k if k in valid_date_keys else 20180101
        )

        returns_insert = df_returns[[
            "return_id", "order_id", "order_item_id", "product_key", "seller_key",
            "customer_key", "return_date", "return_date_key", "return_type",
            "return_reason", "refund_amount", "refund_freight", "total_refund",
            "is_damaged_or_defective"
        ]]

        returns_insert.to_sql(
            "fact_returns",
            conn,
            schema="ecommerce",
            if_exists="append",
            index=False
        )
        print(f"Loaded {len(returns_insert)} rows into fact_returns")

        # 4. Load fact_marketing_performance
        print("Loading fact_marketing_performance...")
        df_mkt = pd.read_csv(PROCESSED_DIR / "marketing_transformed.csv")
        dim_camp_keys = pd.read_sql("SELECT campaign_key, campaign_id FROM ecommerce.dim_campaign", conn)
        df_mkt = df_mkt.merge(dim_camp_keys, on="campaign_id", how="inner")

        df_mkt["date_key"] = df_mkt["date_key"].apply(
            lambda k: k if k in valid_date_keys else 20180115
        )

        mkt_insert = df_mkt[[
            "campaign_key", "date_key", "year", "month", "impressions", "clicks",
            "marketing_spend", "leads", "orders", "attributed_revenue",
            "cpc", "ctr", "cvr", "cac", "roas", "roi_pct"
        ]]

        mkt_insert.to_sql(
            "fact_marketing_performance",
            conn,
            schema="ecommerce",
            if_exists="append",
            index=False
        )
        print(f"Loaded {len(mkt_insert)} rows into fact_marketing_performance")

    print("\nMember 3 tables loaded successfully into PostgreSQL!")


if __name__ == "__main__":
    load_member3_tables()

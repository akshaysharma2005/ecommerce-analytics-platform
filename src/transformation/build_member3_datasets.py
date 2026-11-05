"""
Build Member 3 Transformed Datasets:
1. Category Margins (dim_category_margin)
2. Returns & Cancellations (fact_returns)
3. Marketing Campaigns (dim_campaign)
4. Marketing Performance & Attribution (fact_marketing_performance)
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd

PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def build_category_margins():
    """Create category benchmark gross margins and marketplace take rates."""
    products_path = PROCESSED_DIR / "products_transformed.csv"
    df_prod = pd.read_csv(products_path)
    categories = df_prod["product_category_name_english"].fillna(df_prod["product_category_name"]).fillna("unknown").unique()

    # Domain benchmark margins based on e-commerce retail standards
    margin_rules = {
        "health_beauty": (0.42, 0.16),
        "perfumery": (0.45, 0.16),
        "watches_gifts": (0.40, 0.15),
        "bed_bath_table": (0.32, 0.14),
        "sports_leisure": (0.35, 0.15),
        "computers_accessories": (0.22, 0.12),
        "furniture_decor": (0.34, 0.15),
        "cool_stuff": (0.35, 0.15),
        "housewares": (0.30, 0.14),
        "auto": (0.26, 0.13),
        "garden_tools": (0.28, 0.14),
        "toys": (0.36, 0.15),
        "baby": (0.35, 0.15),
        "telephony": (0.20, 0.12),
        "office_furniture": (0.24, 0.13),
        "stationery": (0.38, 0.15),
        "fashion_bags_accessories": (0.48, 0.18),
        "pet_shop": (0.30, 0.14),
        "electronics": (0.18, 0.12),
        "luggage_accessories": (0.42, 0.16),
        "consoles_games": (0.16, 0.10),
        "home_appliances": (0.20, 0.12),
        "small_appliances": (0.22, 0.12),
        "fashion_shoes": (0.46, 0.17),
        "books_general_interest": (0.38, 0.15),
        "books_technical": (0.35, 0.15),
        "furniture_living_room": (0.30, 0.14),
        "air_conditioning": (0.20, 0.12),
        "food_drink": (0.22, 0.12),
        "drinks": (0.24, 0.12),
    }

    records = []
    for cat in sorted(categories):
        gross_margin, commission = margin_rules.get(cat, (0.30, 0.14))
        records.append({
            "category_name": cat,
            "benchmark_gross_margin_pct": gross_margin,
            "marketplace_commission_pct": commission,
            "estimated_handling_cost_pct": 0.03
        })

    df_margins = pd.DataFrame(records)
    out_file = PROCESSED_DIR / "category_margins_transformed.csv"
    df_margins.to_csv(out_file, index=False)
    print(f"Saved {len(df_margins)} category margins to {out_file}")
    return df_margins


def build_returns_dataset():
    """Extract and build fact_returns from orders, items, payments, and reviews."""
    orders = pd.read_csv(PROCESSED_DIR / "orders_transformed.csv")
    items = pd.read_csv(PROCESSED_DIR / "order_items_transformed.csv")
    reviews = pd.read_csv(PROCESSED_DIR / "reviews_transformed.csv")

    # Match orders
    # 1. Canceled and unavailable orders
    canceled_orders = orders[orders["order_status"].isin(["canceled", "unavailable"])].copy()
    
    # 2. Orders with 1-2 star reviews with return/refund/defect keywords
    return_keywords = ["devol", "reembols", "estorno", "defeito", "cancel", "avariad", "estragad", "danificad", "troca", "nao recebi"]
    pattern = "|".join(return_keywords)
    
    complaint_mask = (reviews["review_score"] <= 2) & reviews["review_comment_message"].fillna("").str.lower().str.contains(pattern)
    complaint_reviews = reviews[complaint_mask].copy()

    # Join items
    canceled_items = items.merge(canceled_orders, on="order_id", how="inner")
    canceled_items["return_date"] = pd.to_datetime(canceled_items["order_purchase_timestamp"]).dt.strftime("%Y-%m-%d")
    canceled_items["return_type"] = np.where(
        canceled_items["order_status"] == "canceled",
        "ORDER_CANCELED",
        "ITEM_UNAVAILABLE"
    )
    canceled_items["return_reason"] = np.where(
        canceled_items["order_status"] == "canceled",
        "Customer Canceled Before Delivery",
        "Item Out of Stock / Unavailable"
    )
    canceled_items["is_damaged_or_defective"] = False

    # Review complaint items
    complaint_items = items.merge(complaint_reviews[["order_id", "review_creation_date", "review_comment_message"]], on="order_id", how="inner")
    # exclude if already in canceled_items
    complaint_items = complaint_items[~complaint_items["order_id"].isin(canceled_orders["order_id"])].copy()
    complaint_items["return_date"] = pd.to_datetime(complaint_items["review_creation_date"]).dt.strftime("%Y-%m-%d")
    
    def classify_review(msg):
        msg = str(msg).lower()
        if any(w in msg for w in ["defeito", "avariad", "estragad", "danificad"]):
            return "RETURN_DEFECTIVE", "Product Defect / Damaged in Transit", True
        elif any(w in msg for w in ["devol", "troca"]):
            return "RETURN_EXCHANGE", "Product Return / Exchange Request", False
        elif any(w in msg for w in ["reembols", "estorno", "cancel"]):
            return "RETURN_REFUND", "Refund Requested / Order Cancelation", False
        else:
            return "RETURN_DISSATISFACTION", "Customer Dissatisfaction", False

    classifications = [classify_review(m) for m in complaint_items["review_comment_message"]]
    complaint_items["return_type"] = [c[0] for c in classifications]
    complaint_items["return_reason"] = [c[1] for c in classifications]
    complaint_items["is_damaged_or_defective"] = [c[2] for c in classifications]

    # Combine both sets
    cols = ["order_id", "order_item_id", "product_id", "seller_id", "price", "freight_value", "item_total_value", "return_date", "return_type", "return_reason", "is_damaged_or_defective"]
    all_returns = pd.concat([canceled_items[cols], complaint_items[cols]], ignore_index=True)

    # Clean up duplicates
    all_returns = all_returns.drop_duplicates(subset=["order_id", "order_item_id"])

    # Build surrogate date_key: YYYYMMDD
    all_returns["return_date_dt"] = pd.to_datetime(all_returns["return_date"])
    all_returns["return_date_key"] = all_returns["return_date_dt"].dt.strftime("%Y%m%d").astype(int)
    all_returns["return_id"] = "RET-" + all_returns["order_id"] + "-" + all_returns["order_item_id"].astype(str)
    all_returns["refund_amount"] = all_returns["price"].round(2)
    all_returns["refund_freight"] = all_returns["freight_value"].round(2)
    all_returns["total_refund"] = (all_returns["price"] + all_returns["freight_value"]).round(2)

    final_returns = all_returns[[
        "return_id", "order_id", "order_item_id", "product_id", "seller_id",
        "return_date", "return_date_key", "return_type", "return_reason",
        "refund_amount", "refund_freight", "total_refund", "is_damaged_or_defective"
    ]]

    out_file = PROCESSED_DIR / "returns_transformed.csv"
    final_returns.to_csv(out_file, index=False)
    print(f"Saved {len(final_returns)} returns to {out_file} (Total refund: {final_returns['total_refund'].sum():,.2f} BRL)")
    return final_returns


def build_marketing_datasets():
    """Build campaigns dimension and monthly marketing performance fact table."""
    # Define multi-channel campaigns
    campaigns = [
        {
            "campaign_id": "CMP-SEM-BRD",
            "campaign_name": "Google Ads - Brand Search",
            "channel": "Paid Search",
            "campaign_type": "Brand Defense",
            "target_audience": "Existing & High-Intent Shoppers",
            "share_of_orders": 0.12,
            "target_cvr": 0.075,
            "target_ctr": 0.085,
            "target_cpc": 0.45,
            "roas_multiplier": 14.2
        },
        {
            "campaign_id": "CMP-SEM-GEN",
            "campaign_name": "Google Ads - Shopping & Generic Non-Brand",
            "channel": "Paid Search",
            "campaign_type": "Performance / Acquisition",
            "target_audience": "In-Market Shoppers",
            "share_of_orders": 0.30,
            "target_cvr": 0.032,
            "target_ctr": 0.031,
            "target_cpc": 1.15,
            "roas_multiplier": 7.4
        },
        {
            "campaign_id": "CMP-SOC-PRO",
            "campaign_name": "Meta Ads - Prospecting & Lookalike",
            "channel": "Paid Social",
            "campaign_type": "Customer Acquisition",
            "target_audience": "Lookalike Audiences",
            "share_of_orders": 0.22,
            "target_cvr": 0.021,
            "target_ctr": 0.019,
            "target_cpc": 0.95,
            "roas_multiplier": 5.2
        },
        {
            "campaign_id": "CMP-SOC-RET",
            "campaign_name": "Meta Ads - Dynamic Product Retargeting",
            "channel": "Paid Social",
            "campaign_type": "Retargeting",
            "target_audience": "Cart & Product Abandoners",
            "share_of_orders": 0.14,
            "target_cvr": 0.054,
            "target_ctr": 0.038,
            "target_cpc": 1.10,
            "roas_multiplier": 8.6
        },
        {
            "campaign_id": "CMP-EML-AUT",
            "campaign_name": "Automated Email & Lifecycle Flows",
            "channel": "Email Marketing",
            "campaign_type": "Retention & Repeat",
            "target_audience": "Subscribed Leads & Past Customers",
            "share_of_orders": 0.12,
            "target_cvr": 0.048,
            "target_ctr": 0.042,
            "target_cpc": 0.18,
            "roas_multiplier": 22.5
        },
        {
            "campaign_id": "CMP-AFF-PAR",
            "campaign_name": "Affiliate & Influencer Partner Network",
            "channel": "Affiliate",
            "campaign_type": "Partner Acquisition",
            "target_audience": "Niche Category Audiences",
            "share_of_orders": 0.10,
            "target_cvr": 0.028,
            "target_ctr": 0.025,
            "target_cpc": 0.85,
            "roas_multiplier": 6.8
        }
    ]

    df_camp = pd.DataFrame([{
        "campaign_id": c["campaign_id"],
        "campaign_name": c["campaign_name"],
        "channel": c["channel"],
        "campaign_type": c["campaign_type"],
        "target_audience": c["target_audience"]
    } for c in campaigns])

    camp_file = PROCESSED_DIR / "campaigns_transformed.csv"
    df_camp.to_csv(camp_file, index=False)
    print(f"Saved {len(df_camp)} campaigns to {camp_file}")

    # Load actual monthly orders and revenue to calibrate marketing attribution
    orders_df = pd.read_csv(PROCESSED_DIR / "orders_transformed.csv")
    items_df = pd.read_csv(PROCESSED_DIR / "order_items_transformed.csv")
    ord_items = orders_df.merge(items_df, on="order_id", how="inner")
    ord_items["purchase_dt"] = pd.to_datetime(ord_items["order_purchase_timestamp"])
    ord_items["year"] = ord_items["purchase_dt"].dt.year
    ord_items["month"] = ord_items["purchase_dt"].dt.month

    monthly_stats = ord_items.groupby(["year", "month"]).agg(
        total_orders=("order_id", "nunique"),
        total_revenue=("item_total_value", "sum")
    ).reset_index()

    perf_records = []
    # Retail benchmark average gross margin ~ 30% for ROI calculation
    avg_gross_margin = 0.30

    for _, row in monthly_stats.iterrows():
        y = int(row["year"])
        m = int(row["month"])
        m_orders = int(row["total_orders"])
        m_rev = float(row["total_revenue"])

        # Mid-month date key YYYYMM15
        date_key = int(f"{y}{m:02d}15")

        for c in campaigns:
            c_orders = int(round(m_orders * c["share_of_orders"]))
            if c_orders == 0 and m_orders > 0:
                c_orders = 1
            
            c_rev = round(m_rev * (c["share_of_orders"] * (0.95 + 0.1 * np.random.uniform(0.95, 1.05))), 2)
            c_spend = round(c_rev / c["roas_multiplier"], 2)
            if c_spend < 10.0 and m_orders > 10:
                c_spend = 10.0

            # Clicks from conversion rate
            c_clicks = int(round(c_orders / c["target_cvr"]))
            if c_clicks < c_orders:
                c_clicks = c_orders * 10

            # Impressions from CTR
            c_impr = int(round(c_clicks / c["target_ctr"]))
            c_leads = int(round(c_clicks * 0.28))

            actual_cpc = round(c_spend / max(c_clicks, 1), 2)
            actual_ctr = round(c_clicks / max(c_impr, 1), 4)
            actual_cvr = round(c_orders / max(c_clicks, 1), 4)
            actual_cac = round(c_spend / max(c_orders, 1), 2)
            actual_roas = round(c_rev / max(c_spend, 1), 2)
            actual_roi = round(((c_rev * avg_gross_margin - c_spend) / max(c_spend, 1)) * 100, 2)

            perf_records.append({
                "campaign_id": c["campaign_id"],
                "year": y,
                "month": m,
                "date_key": date_key,
                "impressions": c_impr,
                "clicks": c_clicks,
                "marketing_spend": c_spend,
                "leads": c_leads,
                "orders": c_orders,
                "attributed_revenue": c_rev,
                "cpc": actual_cpc,
                "ctr": actual_ctr,
                "cvr": actual_cvr,
                "cac": actual_cac,
                "roas": actual_roas,
                "roi_pct": actual_roi
            })

    df_perf = pd.DataFrame(perf_records)
    perf_file = PROCESSED_DIR / "marketing_transformed.csv"
    df_perf.to_csv(perf_file, index=False)
    print(f"Saved {len(df_perf)} marketing performance records to {perf_file}")
    print(f"Total marketing spend: {df_perf['marketing_spend'].sum():,.2f} BRL, Attributed revenue: {df_perf['attributed_revenue'].sum():,.2f} BRL")
    return df_perf


if __name__ == "__main__":
    print("=== BUILDING MEMBER 3 DATASETS ===")
    build_category_margins()
    build_returns_dataset()
    build_marketing_datasets()
    print("=== MEMBER 3 DATASETS BUILT SUCCESSFULLY ===")


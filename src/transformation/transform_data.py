
from pathlib import Path
import pandas as pd
import unicodedata


PROCESSED_DATA_DIR = Path("data/processed")


# ============================================================
# CUSTOMER TRANSFORMATION
# ============================================================

def transform_customers():

    df = pd.read_csv(
        PROCESSED_DATA_DIR / "olist_customers_clean.csv"
    )

    return df


# ============================================================
# ORDER TRANSFORMATION
# ============================================================

def transform_orders():

    df = pd.read_csv(
        PROCESSED_DATA_DIR / "olist_orders_clean.csv"
    )

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    return df


# ============================================================
# ORDER ITEM TRANSFORMATION
# ============================================================

def transform_order_items():

    df = pd.read_csv(
        PROCESSED_DATA_DIR / "olist_order_items_clean.csv"
    )

    df["shipping_limit_date"] = pd.to_datetime(
        df["shipping_limit_date"],
        errors="coerce"
    )

    # Calculate item value including freight
    df["item_total_value"] = (
        df["price"] + df["freight_value"]
    )

    return df


# ============================================================
# PAYMENT TRANSFORMATION
# ============================================================

def transform_payments():

    df = pd.read_csv(
        PROCESSED_DATA_DIR / "olist_order_payments_clean.csv"
    )

    return df


# ============================================================
# REVIEW TRANSFORMATION
# ============================================================

def transform_reviews():

    df = pd.read_csv(
        PROCESSED_DATA_DIR / "olist_order_reviews_clean.csv"
    )

    df["review_creation_date"] = pd.to_datetime(
        df["review_creation_date"],
        errors="coerce"
    )

    df["review_answer_timestamp"] = pd.to_datetime(
        df["review_answer_timestamp"],
        errors="coerce"
    )

    return df


# ============================================================
# PRODUCT TRANSFORMATION
# ============================================================

def transform_products():

    df = pd.read_csv(
        PROCESSED_DATA_DIR / "olist_products_clean.csv"
    )

    category_translation = pd.read_csv(
        PROCESSED_DATA_DIR /
        "product_category_name_translation_clean.csv"
    )

    # Add English category names
    df = df.merge(
        category_translation,
        on="product_category_name",
        how="left",
        validate="many_to_one"
    )

    return df


# ============================================================
# SELLER TRANSFORMATION
# ============================================================

def transform_sellers():

    df = pd.read_csv(
        PROCESSED_DATA_DIR / "olist_sellers_clean.csv"
    )

    return df


# ============================================================
# GEOLOCATION TRANSFORMATION
# ============================================================

def transform_geolocation():

    df = pd.read_csv(
        PROCESSED_DATA_DIR / "olist_geolocation_clean.csv"
    )

    return df


# ============================================================
# LOCATION TRANSFORMATION
# ============================================================

def transform_locations():

    print("\nTransforming location data...")

    df = pd.read_csv(
        PROCESSED_DATA_DIR / "olist_geolocation_clean.csv"
    )

    # Normalize city names by removing accents
    def normalize_city(city):

        city = str(city).strip().lower()

        return "".join(
            char
            for char in unicodedata.normalize("NFKD", city)
            if not unicodedata.combining(char)
        )

    df["normalized_city"] = (
        df["geolocation_city"].apply(normalize_city)
    )

    # Find the most frequent city-state combination
    # for every ZIP prefix
    pair_counts = (
        df.groupby(
            [
                "geolocation_zip_code_prefix",
                "geolocation_state",
                "normalized_city"
            ]
        )
        .size()
        .reset_index(name="record_count")
    )

    # Sort records to handle ties consistently
    pair_counts = pair_counts.sort_values(
        by=[
            "geolocation_zip_code_prefix",
            "record_count",
            "geolocation_state",
            "normalized_city"
        ],
        ascending=[True, False, True, True]
    )

    # Select the most frequent city-state pair
    selected_pairs = (
        pair_counts
        .drop_duplicates(
            subset=["geolocation_zip_code_prefix"]
        )
        .rename(
            columns={
                "geolocation_state": "state",
                "normalized_city": "city"
            }
        )
    )

    # Keep records matching the selected city-state pair
    df = df.merge(
        selected_pairs[
            [
                "geolocation_zip_code_prefix",
                "state",
                "city"
            ]
        ],
        left_on=[
            "geolocation_zip_code_prefix",
            "geolocation_state",
            "normalized_city"
        ],
        right_on=[
            "geolocation_zip_code_prefix",
            "state",
            "city"
        ],
        how="inner"
    )

    # Identify valid Brazilian coordinates
    valid_coordinates = (
        df["geolocation_lat"].between(-35, 6)
        & df["geolocation_lng"].between(-75, -32)
    )

    valid_df = df[valid_coordinates].copy()

    # Calculate average coordinates using valid records only
    coordinate_averages = (
        valid_df.groupby("geolocation_zip_code_prefix")
        .agg(
            latitude=("geolocation_lat", "mean"),
            longitude=("geolocation_lng", "mean")
        )
        .reset_index()
    )

    # Retain every ZIP prefix, even if no valid coordinates exist
    locations = selected_pairs[
        [
            "geolocation_zip_code_prefix",
            "city",
            "state"
        ]
    ].merge(
        coordinate_averages,
        on="geolocation_zip_code_prefix",
        how="left"
    )

    # Rename ZIP prefix column
    locations = locations.rename(
        columns={
            "geolocation_zip_code_prefix": "zip_code_prefix"
        }
    )

    # Arrange columns to match dim_location
    locations = locations[
        [
            "zip_code_prefix",
            "latitude",
            "longitude",
            "city",
            "state"
        ]
    ]

    # Match PostgreSQL coordinate precision
    locations["latitude"] = locations["latitude"].round(6)
    locations["longitude"] = locations["longitude"].round(6)

    # Save transformed locations
    output_file = (
        PROCESSED_DATA_DIR / "locations_transformed.csv"
    )

    locations.to_csv(
        output_file,
        index=False
    )

    print("Location rows:", len(locations))
    print(
        "Unique ZIP prefixes:",
        locations["zip_code_prefix"].nunique()
    )

    print(
        "ZIP prefixes without valid coordinates:",
        locations["latitude"].isna().sum()
    )

    print("Saved:", output_file)

    return locations


# ============================================================
# CATEGORY TRANSLATION TRANSFORMATION
# ============================================================

def transform_category_translation():

    df = pd.read_csv(
        PROCESSED_DATA_DIR /
        "product_category_name_translation_clean.csv"
    )

    return df


# ============================================================
# SAVE TRANSFORMED DATASETS
# ============================================================

def save_dataset(df, file_name):

    output_path = (
        PROCESSED_DATA_DIR / file_name
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved: {file_name} "
        f"({len(df):,} rows)"
    )


# ============================================================
# MAIN TRANSFORMATION PIPELINE
# ============================================================

def main():

    print("=" * 70)
    print("STARTING DATA TRANSFORMATION")
    print("=" * 70)

    customers = transform_customers()
    save_dataset(
        customers,
        "customers_transformed.csv"
    )

    orders = transform_orders()
    save_dataset(
        orders,
        "orders_transformed.csv"
    )

    order_items = transform_order_items()
    save_dataset(
        order_items,
        "order_items_transformed.csv"
    )

    payments = transform_payments()
    save_dataset(
        payments,
        "payments_transformed.csv"
    )

    reviews = transform_reviews()
    save_dataset(
        reviews,
        "reviews_transformed.csv"
    )

    products = transform_products()
    save_dataset(
        products,
        "products_transformed.csv"
    )

    sellers = transform_sellers()
    save_dataset(
        sellers,
        "sellers_transformed.csv"
    )

    geolocation = transform_geolocation()
    save_dataset(
        geolocation,
        "geolocation_transformed.csv"
    )

    locations = transform_locations()
    save_dataset(
        locations,
        "locations_transformed.csv"
    )

    category_translation = transform_category_translation()
    save_dataset(
        category_translation,
        "category_translation_transformed.csv"
    )

    print("=" * 70)
    print("DATA TRANSFORMATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

from pathlib import Path
import pandas as pd


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")


def clean_customers():
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_customers_dataset.csv"
    )

    # Remove completely duplicated rows
    df = df.drop_duplicates()

    return df


def clean_orders():
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_orders_dataset.csv"
    )

    # Convert date columns
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

    # Remove completely duplicated rows
    df = df.drop_duplicates()

    return df


def clean_order_items():
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_order_items_dataset.csv"
    )

    df["shipping_limit_date"] = pd.to_datetime(
        df["shipping_limit_date"],
        errors="coerce"
    )

    df = df.drop_duplicates()

    return df


def clean_order_payments():
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_order_payments_dataset.csv"
    )

    df = df.drop_duplicates()

    # Keep zero-installment records unchanged.
    # They will be documented as data-quality exceptions.
    return df


def clean_order_reviews():
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_order_reviews_dataset.csv"
    )

    date_columns = [
        "review_creation_date",
        "review_answer_timestamp"
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    df = df.drop_duplicates()

    return df


def clean_products():
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_products_dataset.csv"
    )

    df = df.drop_duplicates()

    return df


def clean_sellers():
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_sellers_dataset.csv"
    )

    df = df.drop_duplicates()

    return df


def clean_geolocation():
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_geolocation_dataset.csv"
    )

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    return df


def clean_category_translation():
    df = pd.read_csv(
        RAW_DATA_DIR / "product_category_name_translation.csv"
    )

    df = df.drop_duplicates()

    return df


def save_dataset(df, file_name):
    output_path = PROCESSED_DATA_DIR / file_name

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved: {file_name} "
        f"({len(df):,} rows)"
    )


def main():

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=" * 70)
    print("STARTING DATA CLEANING")
    print("=" * 70)

    # Customers
    customers = clean_customers()
    save_dataset(
        customers,
        "olist_customers_clean.csv"
    )

    # Orders
    orders = clean_orders()
    save_dataset(
        orders,
        "olist_orders_clean.csv"
    )

    # Order Items
    order_items = clean_order_items()
    save_dataset(
        order_items,
        "olist_order_items_clean.csv"
    )

    # Payments
    payments = clean_order_payments()
    save_dataset(
        payments,
        "olist_order_payments_clean.csv"
    )

    # Reviews
    reviews = clean_order_reviews()
    save_dataset(
        reviews,
        "olist_order_reviews_clean.csv"
    )

    # Products
    products = clean_products()
    save_dataset(
        products,
        "olist_products_clean.csv"
    )

    # Sellers
    sellers = clean_sellers()
    save_dataset(
        sellers,
        "olist_sellers_clean.csv"
    )

    # Geolocation
    geolocation = clean_geolocation()
    save_dataset(
        geolocation,
        "olist_geolocation_clean.csv"
    )

    # Category Translation
    category_translation = clean_category_translation()
    save_dataset(
        category_translation,
        "product_category_name_translation_clean.csv"
    )

    print("=" * 70)
    print("DATA CLEANING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
    
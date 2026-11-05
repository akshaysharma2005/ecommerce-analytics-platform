
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text, URL


# ============================================================
# CONFIGURATION
# ============================================================

PROCESSED_DATA_DIR = Path("data/processed")

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "ecommerce")


# Build database URL safely, including special password characters
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_engine():

    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )


def test_connection(engine):

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT version();")
        )

        print("\nPostgreSQL connection successful.")
        print(result.fetchone()[0])


# ============================================================
# CSV VALIDATION
# ============================================================

def validate_csv_columns(dataframe, required_columns, filename):

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing columns in {filename}: {missing_columns}"
        )


# ============================================================
# CLEAR EXISTING DATA
# ============================================================

def truncate_tables(connection):

    print("\nClearing existing data...")

    # All tables are explicitly listed.
    # This operation is part of the main transaction.
    connection.execute(
        text("""
            TRUNCATE TABLE
                ecommerce.fact_reviews,
                ecommerce.fact_payments,
                ecommerce.fact_order_items,
                ecommerce.fact_orders,
                ecommerce.dim_location,
                ecommerce.dim_product,
                ecommerce.dim_seller,
                ecommerce.dim_customer,
                ecommerce.dim_date
            RESTART IDENTITY;
        """)
    )

    print("Existing data cleared.")


# ============================================================
# GENERIC TABLE LOADER
# ============================================================

def load_table(connection, dataframe, table_name):

    dataframe.to_sql(
        table_name,
        connection,
        schema="ecommerce",
        if_exists="append",
        index=False,
        chunksize=500
    )

    print(
        f"Loaded {len(dataframe):,} rows "
        f"into ecommerce.{table_name}"
    )


# ============================================================
# SURROGATE KEY VALIDATION
# ============================================================

def check_missing_keys(dataframe, key_column, table_name):

    missing_count = dataframe[key_column].isna().sum()

    if missing_count > 0:

        raise ValueError(
            f"{missing_count} missing {key_column} values "
            f"found while preparing {table_name}. "
            "Loading stopped."
        )

    print(
        f"Surrogate key validation passed for {table_name}."
    )


# ============================================================
# DATE DIMENSION
# ============================================================

def load_date_dimension(connection):

    print("\nLoading dim_date...")

    dates = pd.date_range(
        start="2016-01-01",
        end="2018-12-31",
        freq="D"
    )

    date_dimension = pd.DataFrame({

        "date_key":
            dates.strftime("%Y%m%d").astype(int),

        "full_date":
            dates.date,

        "year":
            dates.year,

        "quarter":
            dates.quarter,

        "month":
            dates.month,

        "month_name":
            dates.strftime("%B"),

        "day":
            dates.day,

        "day_of_week":
            dates.dayofweek,

        "day_name":
            dates.strftime("%A"),

        "week_of_year":
            dates.isocalendar().week.astype(int)
    })

    load_table(
        connection,
        date_dimension,
        "dim_date"
    )


# ============================================================
# DIMENSION TABLES
# ============================================================

def load_dimensions(connection):

    # --------------------------------------------------------
    # DIM CUSTOMER
    # --------------------------------------------------------

    print("\nLoading dim_customer...")

    customers = pd.read_csv(
        PROCESSED_DATA_DIR / "customers_transformed.csv"
    )

    validate_csv_columns(
        customers,
        [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state"
        ],
        "customers_transformed.csv"
    )

    load_table(
        connection,
        customers,
        "dim_customer"
    )

    # --------------------------------------------------------
    # DIM PRODUCT
    # --------------------------------------------------------

    print("\nLoading dim_product...")

    products = pd.read_csv(
        PROCESSED_DATA_DIR / "products_transformed.csv"
    )

    products = products.rename(
        columns={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length"
        }
    )

    if "product_category_name_english" not in products.columns:

        products["product_category_name_english"] = None

    product_columns = [
        "product_id",
        "product_category_name",
        "product_category_name_english",
        "product_name_length",
        "product_description_length",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    validate_csv_columns(
        products,
        product_columns,
        "products_transformed.csv"
    )

    products = products[product_columns]

    load_table(
        connection,
        products,
        "dim_product"
    )

    # --------------------------------------------------------
    # DIM SELLER
    # --------------------------------------------------------

    print("\nLoading dim_seller...")

    sellers = pd.read_csv(
        PROCESSED_DATA_DIR / "sellers_transformed.csv"
    )

    validate_csv_columns(
        sellers,
        [
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state"
        ],
        "sellers_transformed.csv"
    )

    load_table(
        connection,
        sellers,
        "dim_seller"
    )

    # --------------------------------------------------------
    # DIM LOCATION
    # --------------------------------------------------------

    print("\nLoading dim_location...")

    locations = pd.read_csv(
        PROCESSED_DATA_DIR / "locations_transformed.csv"
    )

    location_columns = [
        "zip_code_prefix",
        "latitude",
        "longitude",
        "city",
        "state"
    ]

    validate_csv_columns(
        locations,
        location_columns,
        "locations_transformed.csv"
    )

    # Convert missing coordinates to Python None.
    # PostgreSQL will store these as NULL.
    for column in ["latitude", "longitude"]:

        locations[column] = (
            locations[column]
            .astype(object)
            .where(locations[column].notna(), None)
        )

    # Validate ZIP prefixes
    if locations["zip_code_prefix"].isna().any():

        raise ValueError(
            "Missing ZIP prefixes found in location data."
        )

    if locations["zip_code_prefix"].duplicated().any():

        raise ValueError(
            "Duplicate ZIP prefixes found in location data."
        )

    # Validate city and state
    if locations[["city", "state"]].isna().any().any():

        raise ValueError(
            "Missing city or state found in location data."
        )

    # Correct row-by-row coordinate validation
    mismatched_coordinates = (
        locations["latitude"].isna()
        != locations["longitude"].isna()
    )

    if mismatched_coordinates.any():

        raise ValueError(
            "Latitude and longitude must both be missing "
            "or both present in every row."
        )

    print(
        f"Location validation passed: {len(locations):,} rows."
    )

    locations = locations[location_columns]

    load_table(
        connection,
        locations,
        "dim_location"
    )


# ============================================================
# FACT TABLES
# ============================================================

def load_facts(connection):

    # ========================================================
    # FACT ORDERS
    # ========================================================

    print("\nLoading fact_orders...")

    orders = pd.read_csv(
        PROCESSED_DATA_DIR / "orders_transformed.csv"
    )

    validate_csv_columns(
        orders,
        [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ],
        "orders_transformed.csv"
    )

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:

        orders[column] = pd.to_datetime(
            orders[column],
            errors="coerce"
        )

    # Get customer surrogate keys
    customer_keys = pd.read_sql(
        text("""
            SELECT
                customer_key,
                customer_id
            FROM ecommerce.dim_customer
        """),
        connection
    )

    orders = orders.merge(
        customer_keys,
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    check_missing_keys(
        orders,
        "customer_key",
        "fact_orders"
    )

    # Generate purchase date key
    orders["purchase_date_key"] = (
        orders["order_purchase_timestamp"]
        .dt.strftime("%Y%m%d")
        .astype("Int64")
    )

    check_missing_keys(
        orders,
        "purchase_date_key",
        "fact_orders purchase date"
    )

    # Validate purchase date keys against dim_date
    date_keys = pd.read_sql(
        text("""
            SELECT date_key
            FROM ecommerce.dim_date
        """),
        connection
    )

    valid_date_keys = set(date_keys["date_key"])

    invalid_dates = ~orders["purchase_date_key"].isin(
        valid_date_keys
    )

    if invalid_dates.any():

        raise ValueError(
            f"{invalid_dates.sum()} purchase dates "
            "do not exist in dim_date."
        )

    orders = orders[
        [
            "order_id",
            "customer_key",
            "order_status",
            "purchase_date_key",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    ]

    load_table(
        connection,
        orders,
        "fact_orders"
    )

    # ========================================================
    # FACT ORDER ITEMS
    # ========================================================

    print("\nLoading fact_order_items...")

    order_items = pd.read_csv(
        PROCESSED_DATA_DIR / "order_items_transformed.csv"
    )

    validate_csv_columns(
        order_items,
        [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "shipping_limit_date",
            "price",
            "freight_value",
            "item_total_value"
        ],
        "order_items_transformed.csv"
    )

    products = pd.read_sql(
        text("""
            SELECT
                product_key,
                product_id
            FROM ecommerce.dim_product
        """),
        connection
    )

    sellers = pd.read_sql(
        text("""
            SELECT
                seller_key,
                seller_id
            FROM ecommerce.dim_seller
        """),
        connection
    )

    order_items = order_items.merge(
        products,
        on="product_id",
        how="left",
        validate="many_to_one"
    )

    order_items = order_items.merge(
        sellers,
        on="seller_id",
        how="left",
        validate="many_to_one"
    )

    check_missing_keys(
        order_items,
        "product_key",
        "fact_order_items"
    )

    check_missing_keys(
        order_items,
        "seller_key",
        "fact_order_items"
    )

    # Validate order references
    valid_order_ids = pd.read_sql(
        text("""
            SELECT order_id
            FROM ecommerce.fact_orders
        """),
        connection
    )

    missing_orders = ~order_items["order_id"].isin(
        valid_order_ids["order_id"]
    )

    if missing_orders.any():

        raise ValueError(
            f"{missing_orders.sum()} order item records "
            "refer to unknown orders."
        )

    order_items["shipping_limit_date"] = pd.to_datetime(
        order_items["shipping_limit_date"],
        errors="coerce"
    )

    order_items = order_items[
        [
            "order_id",
            "order_item_id",
            "product_key",
            "seller_key",
            "shipping_limit_date",
            "price",
            "freight_value",
            "item_total_value"
        ]
    ]

    load_table(
        connection,
        order_items,
        "fact_order_items"
    )

    # ========================================================
    # FACT PAYMENTS
    # ========================================================

    print("\nLoading fact_payments...")

    payments = pd.read_csv(
        PROCESSED_DATA_DIR / "payments_transformed.csv"
    )

    validate_csv_columns(
        payments,
        [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value"
        ],
        "payments_transformed.csv"
    )

    # Validate order references
    missing_payments = ~payments["order_id"].isin(
        valid_order_ids["order_id"]
    )

    if missing_payments.any():

        raise ValueError(
            f"{missing_payments.sum()} payment records "
            "refer to unknown orders."
        )

    payments = payments[
        [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value"
        ]
    ]

    load_table(
        connection,
        payments,
        "fact_payments"
    )

    # ========================================================
    # FACT REVIEWS
    # ========================================================

    print("\nLoading fact_reviews...")

    reviews = pd.read_csv(
        PROCESSED_DATA_DIR / "reviews_transformed.csv"
    )

    validate_csv_columns(
        reviews,
        [
            "review_id",
            "order_id",
            "review_score",
            "review_comment_title",
            "review_comment_message",
            "review_creation_date",
            "review_answer_timestamp"
        ],
        "reviews_transformed.csv"
    )

    # Validate order references
    missing_reviews = ~reviews["order_id"].isin(
        valid_order_ids["order_id"]
    )

    if missing_reviews.any():

        raise ValueError(
            f"{missing_reviews.sum()} review records "
            "refer to unknown orders."
        )

    reviews["review_creation_date"] = pd.to_datetime(
        reviews["review_creation_date"],
        errors="coerce"
    )

    reviews["review_answer_timestamp"] = pd.to_datetime(
        reviews["review_answer_timestamp"],
        errors="coerce"
    )

    reviews = reviews[
        [
            "review_id",
            "order_id",
            "review_score",
            "review_comment_title",
            "review_comment_message",
            "review_creation_date",
            "review_answer_timestamp"
        ]
    ]

    load_table(
        connection,
        reviews,
        "fact_reviews"
    )


# ============================================================
# FINAL ROW COUNT VALIDATION
# ============================================================

def verify_table_counts(connection):

    print("\nVerifying database row counts...")

    expected_counts = {

        "dim_customer": 99441,
        "dim_product": 32951,
        "dim_seller": 3095,
        "dim_location": 19015,
        "dim_date": 1096,

        "fact_orders": 99441,
        "fact_order_items": 112650,
        "fact_payments": 103886,
        "fact_reviews": 99224
    }

    for table_name, expected_count in expected_counts.items():

        actual_count = connection.execute(
            text(
                f"SELECT COUNT(*) FROM ecommerce.{table_name}"
            )
        ).scalar_one()

        print(
            f"{table_name}: {actual_count:,} rows"
        )

        if actual_count != expected_count:

            raise ValueError(
                f"Row count mismatch in {table_name}. "
                f"Expected {expected_count}, got {actual_count}."
            )

    print("\nAll table row counts verified.")


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("POSTGRESQL DATA LOADING")
    print("=" * 70)

    engine = get_engine()

    try:

        test_connection(engine)

        print("\nStarting database loading transaction...")

        # All changes are committed together.
        # Any failure causes a complete rollback.
        with engine.begin() as connection:

            truncate_tables(connection)

            print("\n" + "=" * 70)
            print("LOADING DATE DIMENSION")
            print("=" * 70)

            load_date_dimension(connection)

            print("\n" + "=" * 70)
            print("LOADING DIMENSIONS")
            print("=" * 70)

            load_dimensions(connection)

            print("\n" + "=" * 70)
            print("LOADING FACT TABLES")
            print("=" * 70)

            load_facts(connection)

            verify_table_counts(connection)

        print("\n" + "=" * 70)
        print("DATA LOADING COMPLETE")
        print("TRANSACTION COMMITTED SUCCESSFULLY")
        print("=" * 70)

    except Exception:

        print("\nDATA LOADING FAILED.")
        print("The database transaction has been rolled back.")
        raise

    finally:

        engine.dispose()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()

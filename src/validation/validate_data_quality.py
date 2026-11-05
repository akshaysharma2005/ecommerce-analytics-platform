from pathlib import Path
import pandas as pd


RAW_DATA_DIR = Path("data/raw")
VALIDATION_DIR = Path("data/validation")


def check_primary_keys():
    results = []

    # Customers
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_customers_dataset.csv"
    )

    results.append({
        "check": "customer_id uniqueness",
        "status": "PASS" if df["customer_id"].is_unique else "FAIL",
        "details": f"{df['customer_id'].nunique()} unique / {len(df)} rows",
        "dataset": "",
        "column": ""
    })

    # Orders
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_orders_dataset.csv"
    )

    results.append({
        "check": "order_id uniqueness",
        "status": "PASS" if df["order_id"].is_unique else "FAIL",
        "details": f"{df['order_id'].nunique()} unique / {len(df)} rows",
        "dataset": "",
        "column": ""
    })

    # Products
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_products_dataset.csv"
    )

    results.append({
        "check": "product_id uniqueness",
        "status": "PASS" if df["product_id"].is_unique else "FAIL",
        "details": f"{df['product_id'].nunique()} unique / {len(df)} rows",
        "dataset": "",
        "column": ""
    })

    # Sellers
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_sellers_dataset.csv"
    )

    results.append({
        "check": "seller_id uniqueness",
        "status": "PASS" if df["seller_id"].is_unique else "FAIL",
        "details": f"{df['seller_id'].nunique()} unique / {len(df)} rows",
        "dataset": "",
        "column": ""
    })

    return results


def check_missing_values():
    results = []

    csv_files = sorted(
        RAW_DATA_DIR.glob("*.csv")
    )

    for file_path in csv_files:

        df = pd.read_csv(file_path)

        for column in df.columns:

            missing = df[column].isna().sum()

            if missing > 0:

                results.append({
                    "check": "missing values",
                    "status": "INFO",
                    "details": f"{missing} missing values",
                    "dataset": file_path.name,
                    "column": column
                })

    return results


def check_negative_values():
    results = []

    numeric_columns = {
        "olist_order_items_dataset.csv": [
            "price",
            "freight_value"
        ],
        "olist_order_payments_dataset.csv": [
            "payment_value"
        ],
        "olist_products_dataset.csv": [
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]
    }

    for file_name, columns in numeric_columns.items():

        df = pd.read_csv(
            RAW_DATA_DIR / file_name
        )

        for column in columns:

            negative_count = (
                df[column] < 0
            ).sum()

            results.append({
                "check": "negative values",
                "status": (
                    "PASS"
                    if negative_count == 0
                    else "FAIL"
                ),
                "details": (
                    f"{negative_count} negative values"
                ),
                "dataset": file_name,
                "column": column
            })

    return results


def check_review_scores():

    df = pd.read_csv(
        RAW_DATA_DIR / "olist_order_reviews_dataset.csv"
    )

    invalid = (
        (df["review_score"] < 1) |
        (df["review_score"] > 5)
    ).sum()

    return [{
        "check": "review score range",
        "status": "PASS" if invalid == 0 else "FAIL",
        "details": f"{invalid} invalid scores",
        "dataset": "olist_order_reviews_dataset.csv",
        "column": "review_score"
    }]


def check_payment_installments():

    df = pd.read_csv(
        RAW_DATA_DIR / "olist_order_payments_dataset.csv"
    )

    zero_count = (
        df["payment_installments"] == 0
    ).sum()

    negative_count = (
        df["payment_installments"] < 0
    ).sum()

    if negative_count > 0:
        status = "FAIL"
    elif zero_count > 0:
        status = "INFO"
    else:
        status = "PASS"

    return [{
        "check": "payment installments",
        "status": status,
        "details": (
            f"{zero_count} zero values, "
            f"{negative_count} negative values"
        ),
        "dataset": "olist_order_payments_dataset.csv",
        "column": "payment_installments"
    }]


def check_dates():

    results = []

    date_columns = {
        "olist_orders_dataset.csv": [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ],
        "olist_order_items_dataset.csv": [
            "shipping_limit_date"
        ],
        "olist_order_reviews_dataset.csv": [
            "review_creation_date",
            "review_answer_timestamp"
        ]
    }

    for file_name, columns in date_columns.items():

        df = pd.read_csv(
            RAW_DATA_DIR / file_name
        )

        for column in columns:

            parsed = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            invalid = (
                parsed.isna() &
                df[column].notna()
            ).sum()

            results.append({
                "check": "date parsing",
                "status": (
                    "PASS"
                    if invalid == 0
                    else "FAIL"
                ),
                "details": f"{invalid} invalid dates",
                "dataset": file_name,
                "column": column
            })

    return results


def check_geolocation_duplicates():

    df = pd.read_csv(
        RAW_DATA_DIR / "olist_geolocation_dataset.csv"
    )

    duplicates = df.duplicated().sum()

    return [{
        "check": "geolocation duplicate rows",
        "status": "INFO",
        "details": f"{duplicates} duplicate rows",
        "dataset": "olist_geolocation_dataset.csv",
        "column": "entire row"
    }]


def check_foreign_keys():

    results = []

    customers = pd.read_csv(
        RAW_DATA_DIR / "olist_customers_dataset.csv"
    )

    orders = pd.read_csv(
        RAW_DATA_DIR / "olist_orders_dataset.csv"
    )

    products = pd.read_csv(
        RAW_DATA_DIR / "olist_products_dataset.csv"
    )

    sellers = pd.read_csv(
        RAW_DATA_DIR / "olist_sellers_dataset.csv"
    )

    order_items = pd.read_csv(
        RAW_DATA_DIR / "olist_order_items_dataset.csv"
    )

    payments = pd.read_csv(
        RAW_DATA_DIR / "olist_order_payments_dataset.csv"
    )

    reviews = pd.read_csv(
        RAW_DATA_DIR / "olist_order_reviews_dataset.csv"
    )

    # Orders → Customers
    missing_customers = (
        ~orders["customer_id"].isin(
            customers["customer_id"]
        )
    ).sum()

    results.append({
        "check": "orders.customer_id → customers.customer_id",
        "status": (
            "PASS"
            if missing_customers == 0
            else "FAIL"
        ),
        "details": (
            f"{missing_customers} unmatched customer IDs"
        ),
        "dataset": "olist_orders_dataset.csv",
        "column": "customer_id"
    })

    # Order Items → Orders
    missing_orders = (
        ~order_items["order_id"].isin(
            orders["order_id"]
        )
    ).sum()

    results.append({
        "check": "order_items.order_id → orders.order_id",
        "status": (
            "PASS"
            if missing_orders == 0
            else "FAIL"
        ),
        "details": (
            f"{missing_orders} unmatched order IDs"
        ),
        "dataset": "olist_order_items_dataset.csv",
        "column": "order_id"
    })

    # Order Items → Products
    missing_products = (
        ~order_items["product_id"].isin(
            products["product_id"]
        )
    ).sum()

    results.append({
        "check": "order_items.product_id → products.product_id",
        "status": (
            "PASS"
            if missing_products == 0
            else "FAIL"
        ),
        "details": (
            f"{missing_products} unmatched product IDs"
        ),
        "dataset": "olist_order_items_dataset.csv",
        "column": "product_id"
    })

    # Order Items → Sellers
    missing_sellers = (
        ~order_items["seller_id"].isin(
            sellers["seller_id"]
        )
    ).sum()

    results.append({
        "check": "order_items.seller_id → sellers.seller_id",
        "status": (
            "PASS"
            if missing_sellers == 0
            else "FAIL"
        ),
        "details": (
            f"{missing_sellers} unmatched seller IDs"
        ),
        "dataset": "olist_order_items_dataset.csv",
        "column": "seller_id"
    })

    # Payments → Orders
    missing_payment_orders = (
        ~payments["order_id"].isin(
            orders["order_id"]
        )
    ).sum()

    results.append({
        "check": "payments.order_id → orders.order_id",
        "status": (
            "PASS"
            if missing_payment_orders == 0
            else "FAIL"
        ),
        "details": (
            f"{missing_payment_orders} unmatched order IDs"
        ),
        "dataset": "olist_order_payments_dataset.csv",
        "column": "order_id"
    })

    # Reviews → Orders
    missing_review_orders = (
        ~reviews["order_id"].isin(
            orders["order_id"]
        )
    ).sum()

    results.append({
        "check": "reviews.order_id → orders.order_id",
        "status": (
            "PASS"
            if missing_review_orders == 0
            else "FAIL"
        ),
        "details": (
            f"{missing_review_orders} unmatched order IDs"
        ),
        "dataset": "olist_order_reviews_dataset.csv",
        "column": "order_id"
    })

    return results


def main():

    VALIDATION_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    results = []

    results.extend(check_primary_keys())
    results.extend(check_missing_values())
    results.extend(check_negative_values())
    results.extend(check_review_scores())
    results.extend(check_payment_installments())
    results.extend(check_dates())
    results.extend(check_geolocation_duplicates())
    results.extend(check_foreign_keys())

    report = pd.DataFrame(results)

    output_file = (
        VALIDATION_DIR / "data_quality_report.csv"
    )

    report.to_csv(
        output_file,
        index=False
    )

    print("\nDATA QUALITY VALIDATION COMPLETE")
    print(f"Report created: {output_file}")

    print("\nSummary:")
    print(
        report["status"].value_counts()
    )


if __name__ == "__main__":
    main()
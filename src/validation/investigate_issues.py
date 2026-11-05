from pathlib import Path
import pandas as pd


RAW_DATA_DIR = Path("data/raw")


def investigate_payment_installments():
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_order_payments_dataset.csv"
    )

    print("=" * 70)
    print("PAYMENT INSTALLMENTS")
    print("=" * 70)

    print(
        df[df["payment_installments"] <= 0][
            [
                "order_id",
                "payment_sequential",
                "payment_type",
                "payment_installments",
                "payment_value"
            ]
        ]
    )


def investigate_geolocation_duplicates():
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_geolocation_dataset.csv"
    )

    print("\n" + "=" * 70)
    print("GEOLOCATION DUPLICATES")
    print("=" * 70)

    print(f"Total rows: {len(df):,}")
    print(f"Duplicate rows: {df.duplicated().sum():,}")
    print(
        f"Rows after removing exact duplicates: "
        f"{len(df.drop_duplicates()):,}"
    )

    print("\nDuplicate sample:")
    print(
        df[df.duplicated(keep=False)]
        .sort_values(
            by=[
                "geolocation_zip_code_prefix",
                "geolocation_lat",
                "geolocation_lng"
            ]
        )
        .head(20)
    )


def main():
    investigate_payment_installments()
    investigate_geolocation_duplicates()


if __name__ == "__main__":
    main()
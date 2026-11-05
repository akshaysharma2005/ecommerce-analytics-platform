from pathlib import Path
import pandas as pd


RAW_DATA_DIR = Path("data/raw")


df = pd.read_csv(
    RAW_DATA_DIR / "olist_order_payments_dataset.csv"
)

print("PAYMENT INSTALLMENT DISTRIBUTION")
print("=" * 60)

print(
    df["payment_installments"]
    .value_counts()
    .sort_index()
)

print("\nZERO-INSTALLMENT RECORDS")
print("=" * 60)

print(
    df[df["payment_installments"] == 0]
)
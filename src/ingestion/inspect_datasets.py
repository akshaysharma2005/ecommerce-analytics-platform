from pathlib import Path
import pandas as pd


# Project raw-data directory
RAW_DATA_DIR = Path("data/raw")


def inspect_dataset(file_path):
    """Inspect one CSV dataset."""

    print("=" * 80)
    print(f"DATASET: {file_path.name}")
    print("=" * 80)

    df = pd.read_csv(file_path)

    print(f"Rows    : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumn Names:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 3 Rows:")
    print(df.head(3))

    print()


def main():
    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found in data/raw/")
        return

    print(f"Found {len(csv_files)} CSV files.\n")

    for file_path in csv_files:
        inspect_dataset(file_path)


if __name__ == "__main__":
    main()
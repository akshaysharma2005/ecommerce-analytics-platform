from pathlib import Path
import pandas as pd


RAW_DATA_DIR = Path("data/raw")
VALIDATION_DIR = Path("data/validation")


def profile_dataset(file_path):
    """Generate dataset-level and column-level profiling information."""

    print("=" * 80)
    print(f"PROFILING: {file_path.name}")
    print("=" * 80)

    df = pd.read_csv(file_path)

    # Dataset-level information
    dataset_profile = {
        "dataset": file_path.name,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "duplicate_rows": df.duplicated().sum(),
    }

    # Column-level information
    column_profiles = []

    for column in df.columns:

        series = df[column]

        profile = {
            "dataset": file_path.name,
            "column": column,
            "data_type": str(series.dtype),
            "rows": len(series),
            "missing_count": series.isna().sum(),
            "missing_percentage": round(
                series.isna().mean() * 100, 2
            ),
            "unique_values": series.nunique(dropna=True),
        }

        # Numeric statistics
        if pd.api.types.is_numeric_dtype(series):

            profile["min_value"] = series.min()
            profile["max_value"] = series.max()
            profile["mean_value"] = round(series.mean(), 2)
            profile["median_value"] = series.median()

        else:

            profile["min_value"] = None
            profile["max_value"] = None
            profile["mean_value"] = None
            profile["median_value"] = None

        # Date profiling
        column_lower = column.lower()

        if (
            "date" in column_lower
            or "timestamp" in column_lower
        ):

            parsed_dates = pd.to_datetime(
                series,
                errors="coerce"
            )

            profile["date_parse_success"] = (
                parsed_dates.notna().sum()
            )

            profile["date_parse_failure"] = (
                parsed_dates.isna().sum()
            )

            if parsed_dates.notna().any():

                profile["date_min"] = (
                    parsed_dates.min()
                )

                profile["date_max"] = (
                    parsed_dates.max()
                )

            else:

                profile["date_min"] = None
                profile["date_max"] = None

        else:

            profile["date_parse_success"] = None
            profile["date_parse_failure"] = None
            profile["date_min"] = None
            profile["date_max"] = None

        column_profiles.append(profile)

    return dataset_profile, column_profiles


def main():

    VALIDATION_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    csv_files = sorted(
        RAW_DATA_DIR.glob("*.csv")
    )

    if not csv_files:

        print("No CSV files found in data/raw/")
        return

    all_dataset_profiles = []
    all_column_profiles = []

    for file_path in csv_files:

        dataset_profile, column_profiles = (
            profile_dataset(file_path)
        )

        all_dataset_profiles.append(
            dataset_profile
        )

        all_column_profiles.extend(
            column_profiles
        )

    # Convert results to DataFrames
    dataset_df = pd.DataFrame(
        all_dataset_profiles
    )

    column_df = pd.DataFrame(
        all_column_profiles
    )

    # Save reports
    dataset_report_path = (
        VALIDATION_DIR / "dataset_profile.csv"
    )

    column_report_path = (
        VALIDATION_DIR / "column_profile.csv"
    )

    dataset_df.to_csv(
        dataset_report_path,
        index=False
    )

    column_df.to_csv(
        column_report_path,
        index=False
    )

    print("\n" + "=" * 80)
    print("PROFILING COMPLETE")
    print("=" * 80)

    print(
        f"Dataset report : {dataset_report_path}"
    )

    print(
        f"Column report  : {column_report_path}"
    )


if __name__ == "__main__":
    main()
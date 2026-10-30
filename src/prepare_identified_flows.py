from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw_identified_flows"
OUTPUT_PATH = PROJECT_DIR / "data" / "processed" / "identified_flows.parquet"

DROP_COLUMNS = [
    "Fwd Header Length.1",
    "Bwd PSH Flags",
    "Fwd URG Flags",
    "Bwd URG Flags",
    "CWE Flag Count",
    "Fwd Avg Bytes/Bulk",
    "Fwd Avg Packets/Bulk",
    "Fwd Avg Bulk Rate",
    "Bwd Avg Bytes/Bulk",
    "Bwd Avg Packets/Bulk",
    "Bwd Avg Bulk Rate",
]

IDENTIFIER_COLUMNS = [
    "Flow ID",
    "Source IP",
    "Source Port",
    "Destination IP",
    "Destination Port",
    "Protocol",
    "Timestamp",
]


def load_file(path: Path) -> pd.DataFrame:
    """Load one original identified-flow CSV without modifying the source."""
    df = pd.read_csv(path, encoding="latin1", low_memory=False)
    df.columns = df.columns.str.strip()

    if "Label" not in df.columns:
        raise ValueError(f"Label column not found in {path.name}")

    # Remove only rows that have no data in any column.
    df = df.dropna(how="all").copy()

    # Normalize label whitespace and the observed misdecoded dash.
    df["Label"] = (
        df["Label"]
        .astype("string")
        .str.strip()
        .str.replace("ï¿½", "-", regex=False)
        .str.replace("\x96", "-", regex=False)
        .str.replace("\ufffd", "-", regex=False)
    )

    # Exclude rows with no usable label, including trailing empty rows.
    df = df[df["Label"].notna() & df["Label"].ne("")].copy()

    # Remove the previously audited redundant/constant columns.
    df = df.drop(
        columns=[c for c in DROP_COLUMNS if c in df.columns],
        errors="ignore",
    )

    # Replace infinite numeric values with missing values, then remove
    # rows containing invalid numeric feature values.
    numeric_columns = df.select_dtypes(include="number").columns
    df[numeric_columns] = df[numeric_columns].replace(
        [np.inf, -np.inf], np.nan
    )
    df = df.dropna(subset=list(numeric_columns)).copy()

    return df


def main() -> None:
    if not RAW_DIR.is_dir():
        raise FileNotFoundError(f"Dataset directory not found: {RAW_DIR}")

    files = sorted(RAW_DIR.glob("*.csv"))
    if len(files) != 8:
        raise ValueError(f"Expected 8 CSV files; found {len(files)} in {RAW_DIR}")

    frames = []
    for path in files:
        df = load_file(path)
        print(f"{path.name}: {len(df):,} valid rows")
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)

    # Preserve identifiers in the processed file for grouping/auditing.
    # They must be excluded explicitly when constructing model features.
    missing_ids = [c for c in IDENTIFIER_COLUMNS if c not in combined.columns]
    if missing_ids:
        raise ValueError(f"Expected identifier columns are missing: {missing_ids}")

    numeric_columns = combined.select_dtypes(include="number").columns
    for column in numeric_columns:
        combined[column] = pd.to_numeric(
            combined[column], downcast="float"
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    combined.to_parquet(OUTPUT_PATH, index=False)

    print("\nSaved identified-flow dataset:")
    print(f"Path: {OUTPUT_PATH}")
    print(f"Shape: {combined.shape}")
    print(f"Labels: {combined['Label'].nunique()}")
    print(f"Missing values remaining: {int(combined.isna().sum().sum()):,}")
    print(f"Exact duplicate rows: {int(combined.duplicated().sum()):,}")

    # Verify the saved output can be reloaded.
    check = pd.read_parquet(OUTPUT_PATH)
    if check.shape != combined.shape:
        raise RuntimeError(
            f"Reload shape mismatch: wrote {combined.shape}, read {check.shape}"
        )
    print("Reload verification: passed")


if __name__ == "__main__":
    main()

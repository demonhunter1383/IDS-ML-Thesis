from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw_identified_flows"
PROGRESS_PATH = PROJECT_DIR / "results" / "row_removal_counts.txt"


def count_file(path: Path) -> tuple[int, int, int, int, int]:
    df = pd.read_csv(path, encoding="latin1", low_memory=False)
    df.columns = df.columns.str.strip()
    rows_read = len(df)

    if "Label" not in df.columns:
        raise ValueError(f"Label column not found in {path.name}")

    before = len(df)
    df = df.dropna(how="all").copy()
    empty_rows_removed = before - len(df)

    df["Label"] = (
        df["Label"]
        .astype("string")
        .str.strip()
        .str.replace("ï¿½", "-", regex=False)
        .str.replace("\x96", "-", regex=False)
        .str.replace("\ufffd", "-", regex=False)
    )
    before = len(df)
    df = df[df["Label"].notna() & df["Label"].ne("")].copy()
    invalid_labels_removed = before - len(df)

    numeric_columns = df.select_dtypes(include="number").columns
    df[numeric_columns] = df[numeric_columns].replace(
        [np.inf, -np.inf], np.nan
    )
    before = len(df)
    df = df.dropna(subset=list(numeric_columns)).copy()
    invalid_numeric_removed = before - len(df)

    return (
        rows_read,
        empty_rows_removed,
        invalid_labels_removed,
        invalid_numeric_removed,
        len(df),
    )


def main() -> None:
    if not RAW_DIR.is_dir():
        raise FileNotFoundError(f"Dataset directory not found: {RAW_DIR}")

    files = sorted(RAW_DIR.glob("*.csv"))
    if len(files) != 8:
        raise ValueError(f"Expected 8 CSV files; found {len(files)} in {RAW_DIR}")

    totals = [0, 0, 0, 0, 0]
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PROGRESS_PATH.open("a", encoding="utf-8") as progress:
        for path in files:
            counts = count_file(path)
            for index, count in enumerate(counts):
                totals[index] += count
            line = (
                f"{path.name}: rows_read={counts[0]}, "
                f"empty_rows_removed={counts[1]}, "
                f"missing_or_empty_labels_removed={counts[2]}, "
                f"invalid_numeric_rows_removed={counts[3]}, rows_left={counts[4]}"
            )
            print(line)
            progress.write(line + "\n")
            progress.flush()

    print(
        "TOTAL: "
        f"rows_read={totals[0]}, empty_rows_removed={totals[1]}, "
        f"missing_or_empty_labels_removed={totals[2]}, "
        f"invalid_numeric_rows_removed={totals[3]}, rows_left={totals[4]}"
    )


if __name__ == "__main__":
    main()

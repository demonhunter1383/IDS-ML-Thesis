"""Load the identified-flow CIC-IDS2017 dataset for experiments."""

from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_PATH = PROJECT_DIR / "data" / "processed" / "identified_flows.parquet"

LABEL_COLUMN = "Label"

IDENTIFIER_COLUMNS = [
    "Flow ID",
    "Source IP",
    "Source Port",
    "Destination IP",
    "Destination Port",
    "Protocol",
    "Timestamp",
]

FIVE_TUPLE_COLUMNS = [
    "Source IP",
    "Source Port",
    "Destination IP",
    "Destination Port",
    "Protocol",
]


def load(
    path: str | Path = PROCESSED_PATH,
    include_destination_port: bool = True,
) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Load identified flows and separate model features, labels, and groups.

    Parameters
    ----------
    path:
        Path to the processed identified-flow Parquet file.
    include_destination_port:
        Whether Destination Port is included as a model feature.
        The five-tuple grouping key retains it either way.

    Returns
    -------
    X:
        Numeric model features, excluding identifiers other than the
        optionally included Destination Port.
    y:
        Target labels.
    groups:
        Five-tuple keys for group-based splitting. These keys can recur
        at different times and must not be assumed to identify a unique
        flow over the entire dataset.
    """
    df = pd.read_parquet(path)

    required = [LABEL_COLUMN, *IDENTIFIER_COLUMNS]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Required columns missing from dataset: {missing}")

    if df[LABEL_COLUMN].isna().any():
        raise ValueError("The target Label column contains missing values.")

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    excluded_identifiers = [
        column
        for column in IDENTIFIER_COLUMNS
        if column != "Destination Port" or not include_destination_port
    ]

    feature_columns = [
        column
        for column in numeric_columns
        if column != LABEL_COLUMN and column not in excluded_identifiers
    ]

    if not feature_columns:
        raise ValueError("No numeric model features were found.")

    X = df[feature_columns].copy()
    y = df[LABEL_COLUMN].copy()

    groups = pd.Series(
        list(df[FIVE_TUPLE_COLUMNS].itertuples(index=False, name=None)),
        index=df.index,
        name="five_tuple_group",
        dtype="object",
    )

    return X, y, groups

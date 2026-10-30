"""Unit tests for identified-flow CSV preprocessing."""

import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

from prepare_identified_flows import DROP_COLUMNS, load_file


class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = Path(self.temp_dir.name) / "sample.csv"

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_csv(self, df):
        df.to_csv(self.csv_path, index=False, encoding="latin1")
        return load_file(self.csv_path)

    def base_frame(self):
        return pd.DataFrame({
            " Label ": [" BENIGN ", "ATTACK"],
            "Flow ID": ["flow-1", "flow-2"],
            "Source IP": ["10.0.0.1", "10.0.0.2"],
            "Source Port": [1000, 2000],
            "Destination IP": ["10.0.0.8", "10.0.0.9"],
            "Destination Port": [80, 443],
            "Protocol": [6, 6],
            "Timestamp": ["t1", "t2"],
            "Flow Duration": [100.0, 200.0],
            "Fwd Header Length.1": [0, 0],
        })

    def test_strips_column_and_label_whitespace(self):
        result = self.write_csv(self.base_frame())

        self.assertIn("Label", result.columns)
        self.assertNotIn(" Label ", result.columns)
        self.assertEqual(result["Label"].tolist(), ["BENIGN", "ATTACK"])

    def test_normalizes_replacement_character_in_label(self):
        df = self.base_frame()
        # Construct the Unicode replacement character without embedding
        # a non-ASCII character in the PowerShell command.
        df.loc[1, " Label "] = "Web Attack \u00ef\u00bf\u00bd Brute Force"

        result = self.write_csv(df)

        self.assertEqual(
            result.loc[result["Flow ID"] == "flow-2", "Label"].iloc[0],
            "Web Attack - Brute Force",
        )

    def test_removes_empty_labels_and_invalid_numeric_rows(self):
        df = self.base_frame()
        df.loc[1, " Label "] = ""
        df.loc[0, "Flow Duration"] = float("inf")
        df.loc[0, " Label "] = "BENIGN"

        result = self.write_csv(df)

        self.assertEqual(len(result), 0)

    def test_preserves_identifiers_and_drops_configured_columns(self):
        result = self.write_csv(self.base_frame())

        identifiers = [
            "Flow ID", "Source IP", "Source Port",
            "Destination IP", "Destination Port",
            "Protocol", "Timestamp",
        ]
        for column in identifiers:
            self.assertIn(column, result.columns)

        for column in DROP_COLUMNS:
            self.assertNotIn(column, result.columns)

    def test_preserves_duplicate_rows(self):
        df = self.base_frame()
        df = pd.concat([df.iloc[[0]], df.iloc[[0]]], ignore_index=True)

        result = self.write_csv(df)

        self.assertEqual(len(result), 2)
        self.assertEqual(int(result.duplicated().sum()), 1)

    def test_missing_label_column_raises_error(self):
        df = self.base_frame().drop(columns=[" Label "])
        df.to_csv(self.csv_path, index=False, encoding="latin1")

        with self.assertRaisesRegex(ValueError, "Label column not found"):
            load_file(self.csv_path)


if __name__ == "__main__":
    unittest.main()

"""Unit tests for the identified-flow data loader."""

import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

import data


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dataset_path = Path(self.temp_dir.name) / "sample.parquet"

        self.df = pd.DataFrame({
            "Flow ID": ["flow-1", "flow-2", "flow-3"],
            "Source IP": ["10.0.0.1", "10.0.0.2", "10.0.0.1"],
            "Source Port": [1000, 2000, 1000],
            "Destination IP": ["10.0.0.8", "10.0.0.9", "10.0.0.8"],
            "Destination Port": [80, 443, 80],
            "Protocol": [6, 6, 6],
            "Timestamp": [
                "2017-07-03 08:00:00",
                "2017-07-03 08:01:00",
                "2017-07-03 08:02:00",
            ],
            "Label": ["BENIGN", "ATTACK", "BENIGN"],
            "Flow Duration": [100.0, 200.0, 300.0],
            "Total Fwd Packets": [2, 4, 6],
        })
        self.df.to_parquet(self.dataset_path, index=False)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_returns_features_labels_and_groups(self):
        X, y, groups = data.load(self.dataset_path)

        self.assertEqual(X.shape, (3, 3))
        self.assertEqual(y.tolist(), ["BENIGN", "ATTACK", "BENIGN"])
        self.assertEqual(len(groups), 3)
        self.assertEqual(
            groups.iloc[0],
            ("10.0.0.1", 1000, "10.0.0.8", 80, 6),
        )

    def test_destination_port_can_be_excluded(self):
        X_with_port, y_with_port, groups_with_port = data.load(
            self.dataset_path, include_destination_port=True
        )
        X_without_port, y_without_port, groups_without_port = data.load(
            self.dataset_path, include_destination_port=False
        )

        self.assertIn("Destination Port", X_with_port.columns)
        self.assertNotIn("Destination Port", X_without_port.columns)
        self.assertEqual(X_with_port.shape[1] - X_without_port.shape[1], 1)
        self.assertTrue(y_with_port.equals(y_without_port))
        self.assertTrue(groups_with_port.equals(groups_without_port))

    def test_other_identifier_columns_are_excluded(self):
        X, _, _ = data.load(self.dataset_path)

        for column in [
            "Flow ID", "Source IP", "Source Port",
            "Destination IP", "Protocol", "Timestamp",
        ]:
            self.assertNotIn(column, X.columns)

    def test_missing_required_column_raises_error(self):
        broken = self.df.drop(columns=["Source IP"])
        broken_path = Path(self.temp_dir.name) / "missing_column.parquet"
        broken.to_parquet(broken_path, index=False)

        with self.assertRaisesRegex(ValueError, "Required columns missing"):
            data.load(broken_path)

    def test_missing_label_raises_error(self):
        broken = self.df.copy()
        broken.loc[1, "Label"] = None
        broken_path = Path(self.temp_dir.name) / "missing_label.parquet"
        broken.to_parquet(broken_path, index=False)

        with self.assertRaisesRegex(ValueError, "target Label"):
            data.load(broken_path)


if __name__ == "__main__":
    unittest.main()

"""Processing tests for the refactored data pipeline."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lingvoviz.processing.finalize import finalize_merged_dataset


class ProcessingTests(unittest.TestCase):
    def test_finalize_renames_legacy_columns(self) -> None:
        dataframe = pd.DataFrame(
            {
                "Name_x": ["Aari"],
                "Name_y": ["Aari"],
                "Longtitude": [36.57],
                "Latitude": [5.95],
                "Speakers": [999999],
            }
        )

        final_df = finalize_merged_dataset(dataframe)

        self.assertIn("Name", final_df.columns)
        self.assertIn("Longitude", final_df.columns)
        self.assertNotIn("Name_x", final_df.columns)
        self.assertNotIn("Name_y", final_df.columns)


if __name__ == "__main__":
    unittest.main()

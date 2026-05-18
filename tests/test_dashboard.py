"""Smoke tests for dashboard data handling."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lingvoviz.dashboard.data import load_dashboard_dataset
from lingvoviz.dashboard.figures import build_map_figure


class DashboardTests(unittest.TestCase):
    def test_dashboard_dataset_uses_clean_name_column(self) -> None:
        dataframe = load_dashboard_dataset()
        self.assertIn("Name", dataframe.columns)
        self.assertNotIn("Name_x", dataframe.columns)

    def test_map_search_returns_data_for_known_language(self) -> None:
        dataframe = load_dashboard_dataset()
        figure = build_map_figure(dataframe, search_value="Aari")
        self.assertGreater(len(figure.data), 0)


if __name__ == "__main__":
    unittest.main()

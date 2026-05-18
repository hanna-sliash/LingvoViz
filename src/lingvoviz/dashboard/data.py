"""Dataset loading helpers for the Dash app."""

from __future__ import annotations

import pandas as pd

from lingvoviz.paths import FINAL_DATA_FILE
from lingvoviz.processing.finalize import finalize_merged_dataset


def load_dashboard_dataset() -> pd.DataFrame:
    """Load and normalize the processed dataset for dashboard use."""
    df = pd.read_csv(FINAL_DATA_FILE)
    return finalize_merged_dataset(df)

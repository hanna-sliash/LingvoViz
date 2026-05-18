"""Finalize the merged dataset for dashboard consumption."""

from __future__ import annotations

import pandas as pd


def finalize_merged_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize merged columns into a cleaner dashboard-ready schema."""
    final_df = df.copy()
    final_df = final_df.drop(columns=["Name_y"], errors="ignore")

    rename_map = {
        "Name_x": "Name",
        "Longtitude": "Longitude",
    }
    final_df = final_df.rename(columns=rename_map)
    final_df = final_df.dropna(subset=["Name"])

    numeric_columns = ["Speakers", "Child dialects", "Latitude", "Longitude"]
    for column in numeric_columns:
        if column in final_df.columns:
            final_df[column] = pd.to_numeric(final_df[column], errors="coerce")

    return final_df.reset_index(drop=True)

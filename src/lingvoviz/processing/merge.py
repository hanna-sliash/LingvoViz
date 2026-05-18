"""Merge raw UNESCO and Glottolog data into a unified dataset."""

from __future__ import annotations

import pandas as pd

from lingvoviz.paths import GLOTTOLOG_RAW_FILE, MERGED_DATA_FILE, UNESCO_RAW_FILE
from lingvoviz.processing.clean import clean_glottolog_dataframe, clean_unesco_dataframe


def merge_datasets(unesco_df: pd.DataFrame, glottolog_df: pd.DataFrame) -> pd.DataFrame:
    """Merge UNESCO and Glottolog datasets on Glottocode."""
    return pd.merge(
        unesco_df,
        glottolog_df,
        how="right",
        on="Glottocode",
        sort=False,
        validate="many_to_one",
    )


def build_merged_dataset(
    unesco_path: str = str(UNESCO_RAW_FILE),
    glottolog_path: str = str(GLOTTOLOG_RAW_FILE),
) -> pd.DataFrame:
    """Load, clean, and merge the raw UNESCO and Glottolog CSV files."""
    unesco_df = clean_unesco_dataframe(pd.read_csv(unesco_path, header=0))
    glottolog_df = clean_glottolog_dataframe(pd.read_csv(glottolog_path, header=0))
    return merge_datasets(unesco_df, glottolog_df)


def save_merged_dataset(df: pd.DataFrame, output_path: str = str(MERGED_DATA_FILE)) -> None:
    """Persist the merged intermediate dataset."""
    df.to_csv(output_path, index=False)


def build_processed_dataset() -> pd.DataFrame:
    """Convenience wrapper used by runner scripts."""
    return build_merged_dataset()

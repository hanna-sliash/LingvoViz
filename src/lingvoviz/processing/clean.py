"""Cleaning helpers for raw UNESCO and Glottolog datasets."""

from __future__ import annotations

import numpy as np
import pandas as pd


MISSING_MARKERS = ("N/A", "<NA>")


def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replace known missing markers and remove duplicate rows."""
    cleaned = df.copy()
    cleaned.replace(list(MISSING_MARKERS), np.nan, inplace=True)
    cleaned.drop_duplicates(inplace=True)
    return cleaned


def drop_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop CSV index columns created by previous notebook exports."""
    unnamed_columns = [column for column in df.columns if column.startswith("Unnamed:")]
    return df.drop(columns=unnamed_columns, errors="ignore")


def coerce_string_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Cast selected columns to pandas string dtype when present."""
    cleaned = df.copy()
    available_columns = [column for column in columns if column in cleaned.columns]
    if available_columns:
        cleaned[available_columns] = cleaned[available_columns].astype("string")
    return cleaned


def clean_unesco_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the UNESCO-specific cleanup steps from the original script."""
    cleaned = clean_missing_values(df)
    cleaned = drop_unnamed_columns(cleaned)
    cleaned = coerce_string_columns(
        cleaned, ["Name", "Status", "Link", "Glottocode", "Country"]
    )
    cleaned = cleaned.dropna(subset=["Status", "Glottocode", "Country"], how="all")
    return cleaned


def clean_glottolog_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the Glottolog-specific cleanup steps from the original script."""
    cleaned = clean_missing_values(df)
    cleaned = drop_unnamed_columns(cleaned)
    cleaned = coerce_string_columns(
        cleaned,
        ["Name", "Top-level family", "ISO-639-3", "Glottocode", "Macroarea"],
    )
    cleaned = cleaned.dropna(subset=["Name", "Glottocode"], how="all")
    return cleaned

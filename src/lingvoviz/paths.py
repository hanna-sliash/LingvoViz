"""Central project paths."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"

UNESCO_RAW_FILE = RAW_DATA_DIR / "UNESCO_languages.csv"
GLOTTOLOG_RAW_FILE = RAW_DATA_DIR / "Glottolog_languages.csv"
MERGED_DATA_FILE = INTERIM_DATA_DIR / "merged_languages.csv"
FINAL_DATA_FILE = PROCESSED_DATA_DIR / "final_dataset.csv"


def ensure_data_directories() -> None:
    """Create expected data directories when they are missing."""
    for directory in (RAW_DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR):
        directory.mkdir(parents=True, exist_ok=True)

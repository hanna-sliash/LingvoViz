"""Run the Glottolog scraper and save raw output."""

from __future__ import annotations

from _bootstrap import bootstrap

bootstrap()

from lingvoviz.paths import GLOTTOLOG_RAW_FILE, ensure_data_directories
from lingvoviz.scraping.glottolog import scrape_glottolog_languages


def main() -> None:
    ensure_data_directories()
    df = scrape_glottolog_languages()
    df.to_csv(GLOTTOLOG_RAW_FILE, index=False)
    print(f"Saved Glottolog data to {GLOTTOLOG_RAW_FILE}")


if __name__ == "__main__":
    main()

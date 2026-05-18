"""Run the UNESCO scraper and save raw output."""

from __future__ import annotations

from _bootstrap import bootstrap

bootstrap()

from lingvoviz.paths import UNESCO_RAW_FILE, ensure_data_directories
from lingvoviz.scraping.unesco import scrape_unesco_languages


def main() -> None:
    ensure_data_directories()
    df = scrape_unesco_languages()
    df.to_csv(UNESCO_RAW_FILE, index=False)
    print(f"Saved UNESCO data to {UNESCO_RAW_FILE}")


if __name__ == "__main__":
    main()

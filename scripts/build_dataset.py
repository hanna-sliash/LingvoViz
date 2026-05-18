"""Build the processed dashboard dataset from the raw CSV exports."""

from __future__ import annotations

from _bootstrap import bootstrap

bootstrap()

from lingvoviz.paths import FINAL_DATA_FILE, MERGED_DATA_FILE, ensure_data_directories
from lingvoviz.processing.finalize import finalize_merged_dataset
from lingvoviz.processing.merge import build_processed_dataset, save_merged_dataset


def main() -> None:
    ensure_data_directories()
    merged_df = build_processed_dataset()
    save_merged_dataset(merged_df, str(MERGED_DATA_FILE))

    final_df = finalize_merged_dataset(merged_df)
    final_df.to_csv(FINAL_DATA_FILE, index=False)

    print(f"Merged dataset saved to {MERGED_DATA_FILE}")
    print(f"Final dataset saved to {FINAL_DATA_FILE}")


if __name__ == "__main__":
    main()

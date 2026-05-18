# LingvoViz: Languages of the World

LingvoViz is a dashboard project that explores global linguistic diversity using
data from the UNESCO Atlas of World Languages and Glottolog.

The repository separates exploratory notebook-style files from the reusable
application code:

- `notebooks/` keeps the original numbered scripts unchanged as historical,
  exploratory references.
- `src/lingvoviz/` contains the refactored scraping, processing, and dashboard
  modules.
- `scripts/` contains thin entrypoints for running the pipeline and the app.
- `data/raw`, `data/interim`, and `data/processed` reflect the stages of the
  data pipeline.

## Installation

1. Clone the repository:
   `git clone https://github.com/hanna-sliash/LingvoViz.git`
2. Install dependencies:
   `pip install -r requirements.txt`

## Usage

### Build the processed dataset from the existing raw CSV files

```bash
python scripts/build_dataset.py
```

### Run the dashboard locally

```bash
python scripts/run_dashboard.py
```

Then open `http://127.0.0.1:8050/`.

## Project Structure

```text
LingvoViz/
├─ data/
│  ├─ raw/
│  ├─ interim/
│  └─ processed/
├─ notebooks/
├─ scripts/
├─ src/
│  └─ lingvoviz/
│     ├─ dashboard/
│     ├─ processing/
│     ├─ scraping/
│     ├─ config.py
│     └─ paths.py
└─ tests/
```

## Deployment note

The dashboard app exposes `server` from [app.py](/C:/Users/hslia/OneDrive/Desktop/LingvoViz/app.py)
so services like Render can use a start command such as:

```bash
gunicorn app:server
```

## Acknowledgments

- UNESCO World Atlas of Languages
- Glottolog 5.1

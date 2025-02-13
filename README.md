# LingvoViz: Languages of the World
This project comprehensively and interactively illustrates linguistic diversity of the world by using data from 2 data sets - UNESCO Atlas of World Languages and Glottolog. This is achieved by means of web scraping and an interactive dashboard. 

## Installation
1. Clone the repository: `git clone https://github.com/hanna-sliash/LingvoViz.git`
2. Install dependencies: `pip install -r requirements.txt`

## Usage
1. Run the scripts in `src/` in order of numbering to collect and clean the data and to run the dashboard.
3. Open the dashboard in your browser at `http://127.0.0.1:8050/`.

## File Structure
- `data/`: Raw and cleaned datasets.
- `src/`: Scripts for scraping, cleaning and dashboard

## Acknowledgments
- Data sourced from [Glottolog](https://glottolog.org/glottolog/language) and [UNESCO WAL](https://en.wal.unesco.org/discover/languages).
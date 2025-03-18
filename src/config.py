URL_UNESCO  = "https://en.wal.unesco.org/discover/languages?page={current_page}"
URL_GLOTTOLOG = "https://glottolog.org/glottolog/language"
# Exploring UNESCO webpage, I discovered there 277 pages with lists of languages - going beyond this number would mean an infinite loop
UNKNOWN_VALUE = "Unknown"
NOT_AVAILABLE = "N/A"
PAGE_LIMIT = 279
HEADERS = {"User-Agent": "Mozilla/5.0"}
DATA_PATH_UN = "../Data/UNESCO_languages.csv"
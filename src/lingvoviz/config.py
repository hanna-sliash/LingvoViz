"""Application and scraping configuration."""

from __future__ import annotations

DASHBOARD_TITLE = "LingvoViz - Languages of the World Dashboard"

UNKNOWN_VALUE = "Unknown"
NOT_AVAILABLE = "N/A"

REQUEST_TIMEOUT = 20
REQUEST_DELAY_SECONDS = 0.5
MAX_PAGES_SAFETY = 1000

UNESCO_BASE_URL = "https://en.wal.unesco.org/discover/languages"
UNESCO_LANGUAGE_PAGE_URL = "https://en.wal.unesco.org"
UNESCO_MAINTENANCE_MARKERS = (
    "maintenance",
    "temporarily unavailable",
    "service unavailable",
)

GLOTTOLOG_URL = "https://glottolog.org/glottolog/language"

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8050

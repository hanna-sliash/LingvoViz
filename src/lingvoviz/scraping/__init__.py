"""Scraping entrypoints."""

from .glottolog import scrape_glottolog_languages
from .unesco import scrape_unesco_languages

__all__ = ["scrape_glottolog_languages", "scrape_unesco_languages"]

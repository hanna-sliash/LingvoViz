"""UNESCO scraper refactored from the original notebook-style script."""

from __future__ import annotations

import time
import unicodedata
from typing import Any
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag

from lingvoviz.config import (
    MAX_PAGES_SAFETY,
    NOT_AVAILABLE,
    REQUEST_DELAY_SECONDS,
    REQUEST_TIMEOUT,
    UNESCO_BASE_URL,
    UNESCO_LANGUAGE_PAGE_URL,
    UNESCO_MAINTENANCE_MARKERS,
    UNKNOWN_VALUE,
)


class SiteUnavailableError(RuntimeError):
    """Raised when the target site appears unavailable or under maintenance."""


def create_session() -> requests.Session:
    """Create a session with a descriptive user agent."""
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "LingvoViz/1.0 (+https://github.com/hanna-sliash/LingvoViz)"
            )
        }
    )
    return session


def normalize_name(text: str) -> str:
    """Normalize scraped language names to a consistent unicode form."""
    return unicodedata.normalize("NFKD", text.strip())


def fetch_html(session: requests.Session, url: str, timeout: int = REQUEST_TIMEOUT) -> str:
    """Fetch page HTML and surface maintenance mode explicitly."""
    response = session.get(url, timeout=timeout)
    if response.status_code >= 500:
        raise SiteUnavailableError(f"UNESCO returned {response.status_code} for {url}")

    response.encoding = "utf-8"
    html = response.text
    lowered = html.lower()
    if any(marker in lowered for marker in UNESCO_MAINTENANCE_MARKERS):
        raise SiteUnavailableError("UNESCO site appears to be under maintenance.")
    return html


def parse_listing_page(html: str) -> list[dict[str, str]]:
    """Extract high-level language records from a listing page."""
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="node__content clearfix")
    records: list[dict[str, str]] = []

    for card in cards:
        record = parse_language_card(card)
        if record is not None:
            records.append(record)

    return records


def parse_language_card(card: Tag) -> dict[str, str] | None:
    """Extract the summary fields shown in the language listing."""
    name_div = card.find(
        "div",
        class_="field field--name-field-display-title field--type-string "
        "field--label-hidden field__item",
    )
    status_div = card.find(
        "div",
        class_="field field--name-field-language-situation-m field--type-list-string "
        "field--label-hidden field__item",
    )
    link_tag = card.find("a", href=True)

    if link_tag is None:
        return None

    name = normalize_name(name_div.get_text()) if name_div else UNKNOWN_VALUE
    status = status_div.get_text(strip=True) if status_div else UNKNOWN_VALUE
    link = urljoin(UNESCO_LANGUAGE_PAGE_URL, link_tag["href"])

    return {"Name": name, "Status": status, "Link": link}


def parse_language_detail(html: str) -> dict[str, str]:
    """Extract additional fields from an individual language page."""
    soup = BeautifulSoup(html, "html.parser")

    speakers_div = soup.find(
        "div",
        class_="field field--name-field-number field--type-integer "
        "field--label-hidden field__item",
    )
    glottocode_div = soup.find(
        "div",
        class_="field field--name-field-glottocode field--type-string "
        "field--label-inline",
    )
    country_container = soup.find("div", class_="view-countries-associated")

    country = NOT_AVAILABLE
    if isinstance(country_container, Tag):
        country_tag = country_container.find("a", href=True)
        if country_tag is not None:
            country = country_tag.get_text(strip=True)

    glottocode = NOT_AVAILABLE
    if glottocode_div is not None:
        raw_text = glottocode_div.get_text(" ", strip=True)
        if ":" in raw_text:
            glottocode = raw_text.split(":", maxsplit=1)[1].strip()
        else:
            glottocode = raw_text.strip()

    return {
        "Speakers": speakers_div.get_text(strip=True) if speakers_div else NOT_AVAILABLE,
        "Glottocode": glottocode,
        "Country": country,
    }


def scrape_unesco_languages(
    session: requests.Session | None = None,
    max_pages_safety: int = MAX_PAGES_SAFETY,
    delay_seconds: float = REQUEST_DELAY_SECONDS,
) -> pd.DataFrame:
    """Scrape UNESCO languages until the site stops returning new records."""
    session = session or create_session()
    languages_data: list[dict[str, Any]] = []
    seen_links: set[str] = set()

    for page_number in range(max_pages_safety):
        url = f"{UNESCO_BASE_URL}?text=&sort_by=title&page={page_number}"
        html = fetch_html(session, url)
        listing_records = parse_listing_page(html)

        if not listing_records:
            break

        new_records = 0
        for record in listing_records:
            link = record["Link"]
            if link in seen_links:
                continue

            detail_html = fetch_html(session, link)
            record.update(parse_language_detail(detail_html))
            languages_data.append(record)
            seen_links.add(link)
            new_records += 1

        if new_records == 0:
            break

        time.sleep(delay_seconds)
    else:
        raise RuntimeError("Reached the UNESCO safety page limit before termination.")

    return pd.DataFrame(languages_data)

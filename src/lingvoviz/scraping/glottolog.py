"""Glottolog scraper refactored from the original notebook-style script."""

from __future__ import annotations

import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from lingvoviz.config import GLOTTOLOG_URL


def create_webdriver(headless: bool = True) -> webdriver.Chrome:
    """Create a Chrome webdriver configured for Glottolog scraping."""
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--incognito")
    if headless:
        chrome_options.add_argument("--headless=new")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )


def extract_current_table_page(html: str) -> tuple[list[str], list[list[str]]]:
    """Extract headers and rows from the current Glottolog table page."""
    soup = BeautifulSoup(html, "html.parser")
    language_table = soup.find("table", {"id": "Families"})
    if language_table is None:
        raise RuntimeError("Could not find the Glottolog language table.")

    headers = [header.get_text(strip=True) for header in language_table.find_all("th")]
    rows_data: list[list[str]] = []

    for row in language_table.find_all("tr")[1:]:
        columns = row.find_all("td")
        if not columns:
            continue
        rows_data.append([column.get_text(strip=True) for column in columns])

    return headers, rows_data


def scrape_glottolog_languages(headless: bool = True, delay_seconds: float = 2.0) -> pd.DataFrame:
    """Scrape Glottolog language rows using Selenium pagination."""
    driver = create_webdriver(headless=headless)
    all_rows: list[list[str]] = []
    headers: list[str] | None = None

    try:
        driver.get(GLOTTOLOG_URL)
        time.sleep(delay_seconds)

        while True:
            current_headers, current_rows = extract_current_table_page(driver.page_source)
            headers = headers or current_headers
            all_rows.extend(current_rows)

            next_button = driver.find_element("css selector", "li.next")
            if "disabled" in next_button.get_attribute("class"):
                break

            next_button.find_element("css selector", "a").click()
            time.sleep(delay_seconds)
    finally:
        driver.quit()

    if headers is None:
        raise RuntimeError("No headers were collected from Glottolog.")

    return pd.DataFrame(all_rows, columns=headers)

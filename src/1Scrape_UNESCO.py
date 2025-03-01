import time
import unicodedata

import pandas as pd
import requests
from bs4 import BeautifulSoup

current_page = 0
# Defining constants
# Exploring UNESCO webpage, I discovered there 277 pages with lists of languages - going beyond this number would mean an infinite loop
UNKNOWN_VALUE = "Unknown"
NOT_AVAILABLE = "N/A"
PAGE_LIMIT = 277

# empty list to store scraped data
languages_data = []

# loop through UNESCO website to scrape the information
proceed = True
while proceed == True:
    url = f"https://en.wal.unesco.org/discover/languages?text=&sort_by=title&page={current_page}"
    page = requests.get(url)
    page.encoding = "utf-8"

    soup = BeautifulSoup(page.text, "html.parser")

    # if 404 Not found error pops up, the loop will stop

    if soup.title.text == "404 Not Found":
        proceed = False
    else:
        all_languages = soup.find_all("div", class_="node__content clearfix")

        for language in all_languages:
            item = {}

            # Extract the name of the language
            name_div = language.find(
                "div",
                class_="field field--name-field-display-title field--type-string field--label-hidden field__item",
            )
            if name_div:
                name_text = name_div.text.strip()
                item["Name"] = unicodedata.normalize("NFKD", name_text)

            status_div = language.find(
                "div",
                class_="field field--name-field-language-situation-m field--type-list-string field--label-hidden field__item",
            )

            # Extract the status of the language
            if status_div:
                item["Status"] = status_div.text.strip()
            else:
                item["Status"] = UNKNOWN_VALUE

            # Extract the URL
            link_tag = language.find("a")
            if link_tag and "href" in link_tag.attrs:
                item["Link"] = link_tag.attrs["href"]
            else:
                print(f"No link found for language; {item.get('Name', UNKNOWN_VALUE)}")
                continue

            # Extract additional information from language specific pages (number of speakers, glottocode, and country)
            # We need to click on the specific language page and extract the information from there
            language_page = requests.get(item["Link"])
            language_soup = BeautifulSoup(language_page.text, "html.parser")

            # Number of speakers
            speakers_div = language_soup.find(
                "div",
                class_="field field--name-field-number field--type-integer field--label-hidden field__item",
            )
            if speakers_div:
                item["Speakers"] = speakers_div.text.strip()
            else:
                item["Speakers"] = NOT_AVAILABLE

            # Glottocode - an international classification number that is unique for each language and will be later used to join the datasets on it
            glottocode_div = language_soup.find(
                "div",
                class_="field field--name-field-glottocode field--type-string field--label-inline",
            )
            if glottocode_div:
                item["Glottocode"] = glottocode_div.text.strip()[11:]
            else:
                item["Glottocode"] = NOT_AVAILABLE

            # Country
            country_container = language_soup.find(
                "div", class_="view-countries-associated"
            )
            if country_container:
                country_tag = country_container.find("a", href=True)
                if country_tag:
                    item["Country"] = country_tag.text.strip()
                else:
                    item["Country"] = NOT_AVAILABLE
            else:
                item["Country"] = NOT_AVAILABLE

            # Save scraped data
            languages_data.append(item)

    if current_page > PAGE_LIMIT:
        proceed = False
    print(f"Data from page {current_page} saved")
    current_page += 1
    time.sleep(0.5)

# Create a data frame to store the data and save as .csv
df = pd.DataFrame(languages_data)
df.to_csv("./Data/UNESCO_languages.csv")
print("Data saved to CSV")

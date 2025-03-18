import time
import unicodedata
import pandas as pd
import requests
from bs4 import BeautifulSoup
import config

def fetch_webpage(url):
    try:
        response = requests.get(url, headers=config.HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_basic_lang_data(language):
    """Extracts basic info about languages(name, status, URL)"""
    item = {}
    # Extract the name of the language
    name_div = language.find(
        "h2",
        class_="solr-title",
    )
    if name_div:
                name_text = name_div.text.strip()
                item["Name"] = unicodedata.normalize("NFKD", name_text)
    
    # Extract the status of the language
    status_div = language.find(
        "div",
        class_="field field--name-field-language-situation-m field--type-list-string field--label-hidden field__item",
    )
    if status_div:
        item["Status"] = status_div.text.strip()
    else:
        item["Status"] = config.UNKNOWN_VALUE

    # Extract the URL
    link_tag = language.find("a")
    if link_tag and link_tag.has_attr("href"):
        item["Link"] = link_tag.attrs["href"]
    else:
        print(f"No link found for language; {item.get('Name', config.UNKNOWN_VALUE)}")
        return None
    return item
        
def extract_exra_lang_data(item):
    """Extracts extra details from each individual language page."""     
    # Extract additional information from language specific pages (number of speakers, glottocode, and country)
    language_soup = fetch_webpage(item["Link"])
    if not language_soup:
        return item

    # Extract approximate number of speakers
    speakers_div = language_soup.find(
        "div",
        class_="field field--name-field-number field--type-integer field--label-hidden field__item",
    )
    if speakers_div:
        item["Speakers"] = speakers_div.text.strip()
    else:
        item["Speakers"] = config.NOT_AVAILABLE

    # Extract Glottocode - an international classification number that is unique for each language and will be later used to join the datasets on it
    glottocode_div = language_soup.find(
        "div",
        class_="field field--name-field-glottocode field--type-string field--label-inline",
    )
    if glottocode_div:
        item["Glottocode"] = glottocode_div.text.strip()[11:]
    else:
        item["Glottocode"] = config.NOT_AVAILABLE 

    return item


def scrape_unesco():
    """Scraping function to extract languages from UNESCO website"""
        # empty list to store scraped data
    current_page = 0
    languages_data = []

# loop through UNESCO website to scrape the information
    while current_page < config.PAGE_LIMIT:
        url = config.URL_UNESCO.format(current_page=current_page)
            #page.encoding = "utf-8"

        soup = fetch_webpage(url)

        # if 404 Not found error pops up, the loop will stop

        if not soup or (soup.title and soup.title.text == "404 Not Found"):
            break

        all_languages = soup.find_all("div", class_="node__content clearfix")     

        for language in all_languages:
                item = extract_basic_lang_data(language)
                if item:
                    item = extract_exra_lang_data(item)
                    # Debug: print the extracted item
                    print("Extracted item:", item)
                    languages_data.append(item)
        
        print(f"Data from page {current_page} saved")
        current_page += 1
        time.sleep(0.5)

    return languages_data

languages_data = scrape_unesco()

# Check if any items were scraped
if not languages_data:
    print("No language data was scraped. Check your selectors, URL, and page structure.")

# Create a data frame to store the data and save as .csv
df = pd.DataFrame(languages_data)
df.to_csv(config.DATA_PATH_UN, index=False)
print("Data saved to CSV")
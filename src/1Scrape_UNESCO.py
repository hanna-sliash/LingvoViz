import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
import time

current_page = 0
languages_data = []

proceed = True
while(proceed == True):
    url = "https://en.wal.unesco.org/discover/languages?text=&sort_by=title&page="+str(current_page)
    page = requests.get(url)
    page.encoding = "utf-8"

    soup = BeautifulSoup(page.text, "html.parser")

    if soup.title.text == "404 Not Found": 
        proceed = False
    else:
        all_languages = soup.find_all("div", class_="node__content clearfix")

        for language in all_languages:
            item = {}

            # Extract the name of the language 
            name_div = language.find("div", class_="field field--name-field-display-title field--type-string field--label-hidden field__item")
            if name_div:
                name_text = name_div.text.strip()
                item["Name"] = unicodedata.normalize("NFKD", name_text)

            status_div = language.find("div", class_="field field--name-field-language-situation-m field--type-list-string field--label-hidden field__item")
            
            # Extract the status of the language
            if status_div:
                 item["Status"] = status_div.text.strip()
            else:
                 item["Status"] = "Unknown"

        # Extract the URL
            link_tag = language.find("a")
            if link_tag and "href" in link_tag.attrs:
                 item["Link"] = link_tag.attrs["href"]
            else:
                print(f"No link found for language; {item.get("Name", "Unknown")}")
                continue

        #Extract additional information from language specific pages (number of speakers, glottocode, and country)
            language_page = requests.get(item["Link"])
            language_soup = BeautifulSoup(language_page.text, "html.parser")

        #Number of speakers
            speakers_div = language_soup.find("div", class_= "field field--name-field-number field--type-integer field--label-hidden field__item")
            if speakers_div:
                item["Speakers"] = speakers_div.text.strip()
            else:
                item["Speakers"] = "N/A"
        
        #Glottocode
            glottocode_div = language_soup.find("div", class_ = "field field--name-field-glottocode field--type-string field--label-inline")
            if glottocode_div:
                item["Glottocode"] = glottocode_div.text.strip()[11:]
            else:
                item["Glottocode"] = "N/A"

        #Country
            country_container = language_soup.find("div", class_="view-countries-associated")
            if country_container:
                country_tag = country_container.find("a", href = True)
                if country_tag:
                    item["Country"] = country_tag.text.strip()
                else:
                    item["Country"] = "N/A"
            else:
                item["Country"] = "N/A"

        #Save scraped data
            languages_data.append(item)


    if current_page > 277:
        proceed = False
    print(f"Data from page {current_page} saved")
    current_page += 1
    time.sleep(0.5)

df = pd.DataFrame(languages_data)
df.to_csv("./Data/UNESCO_languages.csv")
print("Data saved to CSV")
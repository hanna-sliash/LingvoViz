import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--incognito")

# # Set up Chrome WebDriver with Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# # Open the Glottolog page
url = "https://glottolog.org/glottolog/language"
driver.get(url)
time.sleep(2)  # Wait for page to fully load

print(driver.capabilities["browserVersion"])

# # Get the page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")


language_table = soup.find("table", {"id": "Families"})
if not language_table:
    print("Could not find the language table on the page.")
    driver.quit()

headers = [
    header.text.strip() for header in language_table.find_all("th", class_="sorting")
]

glotto_data = []

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    language_table = soup.find("table", {"id": "Families"})
    rows = language_table.find_all("tr")

    for row in rows[1:]:
        columns = row.find_all("td")
        row_data = [col.text.strip() for col in columns]
        print("Row data:", row_data)
        glotto_data.append(row_data)

    print(f"Scraped {len(language_table)} so far")

    try:
        # Find the <li> element with class "next"
        next_button_li = driver.find_element("css selector", "li.next")

        # Check if the "Next" button is disabled
        if "disabled" in next_button_li.get_attribute("class"):
            print("No more pages to scrape.")
            break

        # Click the <a> element inside the <li> to go to the next page
        next_button_li.find_element("css selector", "a").click()
        time.sleep(5)  # Adjust delay as needed for page loading
    except Exception as e:
        print(f"Error navigating to next page: {e}")
        break  # Exit if there are issues with pagination

df = pd.DataFrame(glotto_data)
print(df)
df.to_csv("./Data/Glottolog_languages.csv")

# Close the WebDriver
driver.quit()

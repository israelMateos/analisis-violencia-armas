import bs4
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

import kaggle


def get_gun_violence_data():
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(
        "jameslko/gun-violence-data", path="data/raw", unzip=True
    )


def get_us_states_codes():
    url = "https://en.wikipedia.org/wiki/ISO_3166-2:US"
    request = requests.get(url)
    soup = bs4.BeautifulSoup(request.text, "html.parser")
    table = soup.find("table")
    table_body = table.find("tbody")

    states = {}
    for row in table_body.find_all("tr"):
        # If the row is a header, skip it
        if row.find("th"):
            continue
        cells = row.find_all("td")
        state_code = cells[0].find("span").text[-2:]
        state_name = cells[1].find("a").text
        states[state_name] = state_code

    return states


def get_datasets():
    get_gun_violence_data()
    get_us_states_codes()

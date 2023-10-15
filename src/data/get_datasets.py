import bs4
import pandas as pd
import requests
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver

load_dotenv(find_dotenv())

import kaggle


def get_gun_violence_data():
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(
        "jameslko/gun-violence-data", path="data/raw", unzip=True
    )


def get_us_states_codes():
    url = "https://en.wikipedia.org/wiki/ISO_3166-2:US"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    table_body = table.find("tbody")

    states = {}
    for row in table_body.find_all("tr"):
        # If the row is a header, skip it
        if row.find("th"):
            continue
        cells = row.find_all("td")
        subcategory = cells[2].text.replace("\n", "")
        # If the row is not a state or a district, skip it
        if subcategory != "State" and subcategory != "District":
            continue
        state_code = cells[0].find("span").text[-2:]
        state_name = cells[1].find("a").text
        states[state_name] = state_code

    return states


def get_poverty_data():
    site = "https://www.povertyusa.org/data"
    states = get_us_states_codes()
    years = ["2015", "2016", "2017", "2018"]

    # The sites uses JavaScript to load the data, so we need to use Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    data = []
    for year in years:
        for state_name, state_code in states.items():
            url = site + f"/{year}/{state_code}"
            driver.get(url)
            # Once the page is loaded, we can use BeautifulSoup to parse the HTML
            page_source = driver.page_source
            soup = bs4.BeautifulSoup(page_source, "html.parser")

            row = [int(year), state_name]
            # Population
            row.append(
                int(
                    soup.find("div", {"class": "simple-stat population stat"})
                    .find("span", {"class": "stat"})
                    .find("span")["data-value"]
                )
            )
            # Population in poverty
            row.append(
                int(
                    soup.find("div", {"class": "simple-stat in-poverty stat"})
                    .find("span", {"class": "stat"})
                    .find("span")["data-value"]
                )
            )
            # Poverty rate
            poverty_rate_section = soup.find(
                "div", {"class": "simple-stat poverty-rate stat"}
            )
            row.append(
                None  # Some states and years don't have data for this
                if poverty_rate_section is None
                else poverty_rate_section.find("span", {"class": "stat"}).find("span")[
                    "data-value"
                ]
            )
            # Median household income, deep poverty rate, median rent, unemployment rate,
            # without health insurance and supplemental poverty measure
            stats = soup.find_all("h2", {"class": "stat h1 font-weight--light"})
            for stat in stats:
                # There are both ints and percentages
                stat = stat.find("span")["data-value"]
                row.append(float(stat) if "." in stat else int(stat))

            data.append(row)

    driver.quit()

    df = pd.DataFrame(
        data,
        columns=[
            "year",
            "state",
            "population",
            "in_poverty",
            "poverty_rate",
            "median_household_income",
            "deep_poverty_rate",
            "median_rent",
            "unemployment_rate",
            "without_health_insurance",
            "supplemental_poverty_measure",
        ],
    )
    df.to_csv("data/raw/poverty_data.csv", index=False)


def get_firearm_laws_data():
    database_url = (
        "https://mail.statefirearmlaws.org/sites/default/files/2020-07/DATABASE_0.xlsx"
    )
    codebook_url = (
        "https://mail.statefirearmlaws.org/sites/default/files/2020-07/codebook_0.xlsx"
    )

    # Download the database
    database = requests.get(database_url)
    with open("data/raw/firearm_laws_database.xlsx", "wb") as f:
        f.write(database.content)

    # Download the codebook
    codebook = requests.get(codebook_url)
    with open("data/raw/firearm_laws_codebook.xlsx", "wb") as f:
        f.write(codebook.content)


def get_datasets():
    get_gun_violence_data()
    get_poverty_data()
    get_firearm_laws_data()

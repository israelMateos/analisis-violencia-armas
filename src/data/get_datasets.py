"""Functions to download the datasets used in the project.

The datasets are downloaded from the following sources:
- Gun violence data: https://www.kaggle.com/jameslko/gun-violence-data
- Poverty data: https://www.povertyusa.org/data
- Firearm laws data: https://statefirearmlaws.org/
"""

import logging
import os
from collections import defaultdict
from datetime import datetime

import bs4
import pandas as pd
import requests
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver

load_dotenv(find_dotenv())

import kaggle  # pylint: disable=wrong-import-position

# Generate a unique timestamp for the log file name
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/get_datasets_{timestamp}.log"

# Configure logging to write to both console and the uniquely named log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(),
    ],
)


def get_gun_violence_data() -> None:
    """Download the gun violence data from Kaggle."""
    logging.info("Downloading the gun violence data...")
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(
        "jameslko/gun-violence-data", path="data/raw", unzip=True
    )
    logging.info("Gun violence data downloaded successfully.")


def get_us_states_codes() -> dict:
    """Get the ISO 3166-2 codes for the US states and districts.

    Returns:
        dict: US states and districts as keys and their codes as values.
    """
    url = "https://en.wikipedia.org/wiki/ISO_3166-2:US"
    response = requests.get(url, timeout=5)
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
        if subcategory not in ("State", "District"):
            continue
        state_code = cells[0].find("span").text[-2:]
        state_name = cells[1].find("a").text
        states[state_name] = state_code

    return states


def get_poverty_data() -> None:
    """Download the poverty data from povertyusa.org."""
    logging.info("Downloading the poverty data...")
    site = "https://www.povertyusa.org/data"
    states = get_us_states_codes()
    years = ["2015", "2016", "2017", "2018"]

    # The sites uses JavaScript to load the data, so we need to use Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    data = defaultdict(list)
    for year in years:
        for state_name, state_code in states.items():
            url = site + f"/{year}/{state_code}"
            driver.get(url)
            # Once the page is loaded, we can use BeautifulSoup to parse the HTML
            soup = bs4.BeautifulSoup(driver.page_source, "html.parser")

            data["year"].append(int(year))
            data["state"].append(state_name)
            # Population
            data["population"].append(
                int(
                    soup.find("div", {"class": "simple-stat population stat"})
                    .find("span", {"class": "stat"})
                    .find("span")["data-value"]
                )
            )
            # Population in poverty
            data["in_poverty"].append(
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
            data["poverty_rate"].append(
                None  # Some states and years don't have data for this
                if poverty_rate_section is None
                else poverty_rate_section.find("span", {"class": "stat"}).find("span")[
                    "data-value"
                ]
            )
            # Median household income, deep poverty rate, median rent, unemployment rate,
            # without health insurance and supplemental poverty measure

            # Some states and years don't have data for these, so we initialize them to None
            stats = {
                "median_household_income": None,
                "deep_poverty_rate": None,
                "median_rent": None,
                "unemployment_rate": None,
                "without_health_insurance": None,
                "supplemental_poverty_measure": None,
            }
            for stat_card in soup.find_all(
                "div", {"class": "stat-card bg-color--gray"}
            ):
                stat_name = stat_card.find("h4").text.replace(" ", "_").lower()
                stat_value = stat_card.find(
                    "h2", {"class": "stat h1 font-weight--light"}
                ).find("span")["data-value"]
                stats[stat_name] = (
                    float(stat_value) if "." in stat_value else int(stat_value)
                )

            for stat_name, stat_value in stats.items():
                data[stat_name].append(stat_value)

    driver.quit()

    df = pd.DataFrame.from_dict(data)
    df.to_csv("data/raw/poverty_data.csv", index=False)
    logging.info("Poverty data downloaded successfully.")


def get_firearm_laws_data() -> None:
    """Download the firearm laws data from statefirearmlaws.org."""
    logging.info("Downloading the firearm laws data...")
    database_url = (
        "https://mail.statefirearmlaws.org/sites/default/files/2020-07/DATABASE_0.xlsx"
    )
    codebook_url = (
        "https://mail.statefirearmlaws.org/sites/default/files/2020-07/codebook_0.xlsx"
    )

    # Download the database
    database = requests.get(database_url, timeout=5)
    with open("data/raw/firearm_laws_database.xlsx", "wb") as f:
        f.write(database.content)

    # Download the codebook
    codebook = requests.get(codebook_url, timeout=5)
    with open("data/raw/firearm_laws_codebook.xlsx", "wb") as f:
        f.write(codebook.content)
    logging.info("Firearm laws data downloaded successfully.")


def get_population_data() -> None:
    """Download the population data from the US Census Bureau."""
    logging.info("Downloading the population data...")
    url = "https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/national/totals/nst-est2019-alldata.csv"
    response = requests.get(url, timeout=5)
    with open("data/raw/population_data.csv", "wb") as f:
        f.write(response.content)
    logging.info("Population data downloaded successfully.")


def get_climate_states_codes() -> None:
    """Get the internal state codes for the climate data."""
    logging.info("Getting the internal state codes for the climate data...")
    url = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/state-readme.txt"
    response = requests.get(url, timeout=5)
    with open("data/raw/climate_state_codes.txt", "w") as f:
        f.write(response.text)
    logging.info("Internal state codes for the climate data downloaded successfully.")


def get_climate_data() -> None:
    """Download the climate data from the National Centers for Environmental Information."""
    logging.info("Downloading the climate data...")

    # Temperature data
    logging.info("Downloading temperature data...")
    url = (
        "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/climdiv-tmpcst-v1.0.0-20231206"
    )
    response = requests.get(url, timeout=5)
    with open("data/raw/temperature_data.txt", "w") as f:
        f.write(response.text)
    logging.info("Temperature data downloaded successfully.")

    # Precipitation data
    logging.info("Downloading precipitation data...")
    url = (
        "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/climdiv-pcpnst-v1.0.0-20231206"
    )
    response = requests.get(url, timeout=5)
    with open("data/raw/precipitation_data.txt", "w") as f:
        f.write(response.text)
    logging.info("Precipitation data downloaded successfully.")

    logging.info("Climate data downloaded successfully.")


def get_datasets() -> None:
    """Download all the datasets to the data/raw directory."""
    logging.info("Downloading the datasets...")
    try:
        get_gun_violence_data()
    except Exception as e:
        logging.error("Error downloading the gun violence data: %s", e)
    try:
        get_poverty_data()
    except Exception as e:
        logging.error("Error downloading the poverty data: %s", e)
    try:
        get_firearm_laws_data()
    except Exception as e:
        logging.error("Error downloading the firearm laws data: %s", e)
    try:
        get_population_data()
    except Exception as e:
        logging.error("Error downloading the population data: %s", e)
    try:
        get_climate_states_codes()
    except Exception as e:
        logging.error("Error downloading the climate state codes: %s", e)
    try:
        get_climate_data()
    except Exception as e:
        logging.error("Error downloading the climate data: %s", e)
    logging.info("All datasets downloaded successfully.")


if __name__ == "__main__":
    get_datasets()

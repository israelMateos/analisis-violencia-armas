"""Module containing functions to generate the final processed data tables from the clean data."""
import logging
import os
from datetime import datetime
from typing import Tuple

import pandas as pd
from pandas import DataFrame

# Generate a unique timestamp for the log file name
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/preprocess_datasets_{timestamp}.log"

# Configure logging to write to both console and the uniquely named log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(),
    ],
)


def load_datasets() -> (
    Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]
):
    """Loads the datasets

    Returns:
        Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]: Datasets
    """
    logging.info("Loading incidents dataset...")
    gun_violence_df = pd.read_csv("data/interim/gun_violence_incidents.csv")
    logging.info("Incidents dataset loaded")

    logging.info("Loading climate dataset...")
    climate_df = pd.read_csv("data/interim/climate_data.csv")
    logging.info("Climate dataset loaded")

    logging.info("Loading poverty dataset...")
    poverty_df = pd.read_csv("data/interim/poverty_data.csv")
    logging.info("Poverty dataset loaded")

    logging.info("Loading firearm laws dataset...")
    firearm_laws_database_df = pd.read_csv("data/interim/firearm_laws_database.csv")
    firearm_laws_codebook_df = pd.read_csv("data/interim/firearm_laws_codebook.csv")
    logging.info("Firearm laws dataset loaded")

    logging.info("Loading population dataset...")
    population_df = pd.read_csv("data/interim/population_data.csv")
    logging.info("Population dataset loaded")

    return (
        gun_violence_df,
        climate_df,
        poverty_df,
        firearm_laws_database_df,
        firearm_laws_codebook_df,
        population_df,
    )


def select_data(
    gun_violence_df: DataFrame,
    climate_df: DataFrame,
    firearm_laws_database_df: DataFrame,
    population_df: DataFrame,
) -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    # Incidents
    gun_violence_df = gun_violence_df[gun_violence_df["year"] != 2018]

    # Climate
    climate_df = climate_df[climate_df["year"] > 2013]
    climate_df = climate_df[climate_df["year"] < 2018]

    # Firearm laws
    firearm_laws_database_df = firearm_laws_database_df[
        firearm_laws_database_df["year"] >= 2013
    ]

    # Population
    regions_to_remove = [
        "United States",
        "Northeast Region",
        "Midwest Region",
        "South Region",
        "West Region",
        "Puerto Rico",
    ]
    selected_years = [2014, 2015, 2016, 2017]
    selected_population_columns = ["name", "year", "popestimate"]

    population_df = population_df[~population_df["name"].isin(regions_to_remove)]
    population_df = population_df[population_df["year"].isin(selected_years)]
    population_df = population_df[selected_population_columns]

    return (
        gun_violence_df,
        climate_df,
        firearm_laws_database_df,
        population_df,
    )


def create_incidents_weekend_table(
    gun_violence_df: DataFrame, population_df: DataFrame
) -> DataFrame:
    """Create a table with the number of incidents per 100000 people per day in weekends for each state and year.

    Args:
        gun_violence_df (DataFrame): Incidents dataset
        population_df (DataFrame): Population dataset

    Returns:
        DataFrame: Table with the number of incidents per 100000 people per day in weekends for each state and year
    """
    # Aggregation of number of incidents by state, year, month and day
    table = (
        gun_violence_df.groupby(["state", "year", "month", "day"])
        .size()
        .reset_index(name="n_incidents")
    )

    # Create column is_weekend
    table["is_weekend"] = table.apply(
        lambda row: 1
        if datetime(row["year"], row["month"], row["day"]).weekday() >= 5
        else 0,
        axis=1,
    )

    # For each state and year, calculate the number of incidents in weekends
    table = (
        table.groupby(["state", "year", "is_weekend"])
        .agg({"n_incidents": ["sum", "count"]})
        .reset_index()
    )
    table.columns = ["state", "year", "is_weekend", "n_incidents", "n_days"]

    # Divide sum by count to get the incidents per day
    table["n_incidents_per_day"] = table["n_incidents"] / table["n_days"]
    table.drop(columns=["n_incidents", "n_days"], inplace=True)

    # Get popestimate from population_df (which is the population) for each state and year and divide the number of incidents per day by 100000 to get the incidents per 100000 people
    table = table.merge(
        population_df, left_on=["state", "year"], right_on=["name", "year"]
    )
    table.drop(columns=["name"], inplace=True)
    table["n_incidents_per_day"] = (
        table["n_incidents_per_day"] / table["popestimate"] * 100000
    )
    table.drop(columns=["popestimate"], inplace=True)

    # Save table to csv
    os.makedirs("data/processed", exist_ok=True)
    table.to_csv("data/processed/incidents_weekend.csv", index=False)

    return table


def create_incidents_climate_table(
    gun_violence_df: DataFrame, climate_df: DataFrame, population_df: DataFrame
) -> DataFrame:
    """Create a table with the number of incidents per 100000 people per month and average temperature and precipitation for each state and year.

    Args:
        gun_violence_df (DataFrame): Incidents dataset
        climate_df (DataFrame): Climate dataset
        population_df (DataFrame): Population dataset

    Returns:
        DataFrame: Table with the number of incidents per 100000 people per month and average temperature and precipitation for each state and year
    """
    # Aggregation of number of incidents by state, year and month
    table = (
        gun_violence_df.groupby(["state", "year", "month"])
        .size()
        .reset_index(name="n_incidents")
    )

    # Add average temperature for each state, year and month
    table = table.merge(climate_df, on=["state", "year", "month"], how="left")

    # Scale the number of incidents by population (per 100,000 inhabitants) using population_df's popestimate column
    table = table.merge(
        population_df, left_on=["state", "year"], right_on=["name", "year"]
    )
    table.drop(columns=["name"], inplace=True)
    table["n_incidents"] = table["n_incidents"] / table["popestimate"] * 100000
    table.drop(columns=["popestimate"], inplace=True)

    # Drop 'District of Columbia' and 'Hawaii' because it has no data for average temperature
    table = table[~table["state"].isin(["District of Columbia", "Hawaii"])]

    # Save table to csv
    os.makedirs("data/processed", exist_ok=True)
    table.to_csv("data/processed/incidents_climate.csv", index=False)

    return table


def create_incidents_poverty_table(
    gun_violence_df: DataFrame, poverty_df: DataFrame, population_df: DataFrame
) -> DataFrame:
    """Create a table with the number of incidents per 100000 people per year and poverty rate for each state and year.

    Args:
        gun_violence_df (DataFrame): Incidents dataset
        poverty_df (DataFrame): Poverty dataset
        population_df (DataFrame): Population dataset

    Returns:
        DataFrame: Table with the number of incidents per 100000 people per year and poverty rate for each state and year
    """
    # Aggregation of number of incidents by state and year
    table = (
        gun_violence_df.groupby(["state", "year"])
        .size()
        .reset_index(name="n_incidents")
    )

    table = table[table["year"] > 2014]

    # Add poverty_rate column to table
    poverty_selected_columns = ["year", "state", "poverty_rate"]
    poverty_df = poverty_df[poverty_selected_columns]
    table = pd.merge(table, poverty_df, on=["state", "year"], how="left")

    # Scale the number of incidents by population (per 100,000 inhabitants) using population_df's popestimate column
    table = table.merge(
        population_df, left_on=["state", "year"], right_on=["name", "year"]
    )
    table.drop(columns=["name"], inplace=True)
    table["n_incidents"] = table["n_incidents"] / table["popestimate"] * 100000
    table.drop(columns=["popestimate"], inplace=True)

    # Save table to csv
    os.makedirs("data/processed", exist_ok=True)
    table.to_csv("data/processed/incidents_population_poverty.csv", index=False)

    return table


def create_incidents_laws_table(
    gun_violence_df: DataFrame,
    firearm_laws_database_df: DataFrame,
    firearm_laws_codebook_df: DataFrame,
    population_df: DataFrame,
) -> DataFrame:
    """Create a table with the number of incidents per 100000 people per year and firearm laws for each state and year.

    Args:
        gun_violence_df (DataFrame): Incidents dataset
        firearm_laws_database_df (DataFrame): Database of firearm laws
        firearm_laws_codebook_df (DataFrame): Codebook of firearm laws
        population_df (DataFrame): Population dataset

    Returns:
        DataFrame: Table with the number of incidents per 100000 people per year and firearm laws for each state and year
    """
    # Aggregation of number of incidents by state and year
    table = (
        gun_violence_df.groupby(["state", "year"])
        .size()
        .reset_index(name="n_incidents")
    )

    # Add popestimate column from population_df to table and scale the number of incidents by population (per 100,000 inhabitants)
    table = table.merge(
        population_df, left_on=["state", "year"], right_on=["name", "year"]
    )
    table.drop(columns=["name"], inplace=True)
    table["n_incidents"] = table["n_incidents"] / table["popestimate"] * 100000
    table.drop(columns=["popestimate"], inplace=True)

    # Add firearm laws columns to table
    table = pd.merge(table, firearm_laws_database_df, on=["state", "year"], how="left")
    table.head()

    # Create new columns for each category_code
    firearm_laws_codebook_selected_columns = ["category_code", "variable_name"]
    firearm_laws_codebook_df = firearm_laws_codebook_df[
        firearm_laws_codebook_selected_columns
    ]
    category_columns = []
    for category_code in firearm_laws_codebook_df["category_code"].unique():
        category_columns.append("laws_" + str(category_code))

    for category_column in category_columns:
        table[category_column] = 0

    # Fill category columns with the corresponding value. For a state and year, check all the variables and add 1 to the corresponding category column if the value is 1
    for index, row in table.iterrows():
        for category_column in category_columns:
            for variable_name in firearm_laws_codebook_df[
                firearm_laws_codebook_df["category_code"] == int(category_column[5:])
            ]["variable_name"]:
                if row[variable_name] == 1:
                    table.at[index, category_column] += 1

    # Drop all the variables columns
    for variable_name in firearm_laws_codebook_df["variable_name"]:
        table.drop(columns=[variable_name], inplace=True)

    # Drop 'District of Columbia' data
    table = table[table["state"] != "District of Columbia"]

    # Save table to csv
    os.makedirs("data/processed", exist_ok=True)
    table.to_csv("data/processed/incidents_firearm_laws.csv", index=False)

    return table


def create_combined_table(
    gun_violence_df: DataFrame,
    climate_df: DataFrame,
    firearm_laws_database_df: DataFrame,
    firearm_laws_codebook_df: DataFrame,
    population_df: DataFrame,
    poverty_df: DataFrame,
) -> DataFrame:
    """Create a table with the number of incidents per 100000 people per year and climate, firearm laws and poverty data for each state and year.

    Args:
        gun_violence_df (DataFrame): Incidents dataset
        climate_df (DataFrame): Climate dataset
        firearm_laws_database_df (DataFrame): Database of firearm laws
        firearm_laws_codebook_df (DataFrame): Codebook of firearm laws
        population_df (DataFrame): Population dataset
        poverty_df (DataFrame): Poverty dataset

    Returns:
        DataFrame: Table with the number of incidents per 100000 people per year and climate, firearm laws and poverty data for each state and year
    """
    # Aggregation of number of incidents by state and year
    table = (
        gun_violence_df.groupby(["state", "year"])
        .size()
        .reset_index(name="n_incidents")
    )

    # Add popestimate column from population_df to table and scale the number of incidents by population (per 100,000 inhabitants)
    table = table.merge(
        population_df, left_on=["state", "year"], right_on=["name", "year"]
    )
    table.drop(columns=["name"], inplace=True)
    table["n_incidents"] = table["n_incidents"] / table["popestimate"] * 100000
    table.drop(columns=["popestimate"], inplace=True)

    ## CLIMATE
    # Aggregation of average temperature and average precipitation by state and year (mean)
    climate_df = climate_df.groupby(["state", "year"]).mean().reset_index()
    climate_df.drop(columns=["month"], inplace=True)

    # Add average temperature column to table
    table = pd.merge(table, climate_df, on=["state", "year"], how="left")

    ## POVERTY
    # Add poverty_rate column to table
    poverty_selected_columns = ["year", "state", "poverty_rate"]
    poverty_df = poverty_df[poverty_selected_columns]
    table = pd.merge(table, poverty_df, on=["state", "year"], how="left")

    ## FIREARM LAWS
    # Add firearm laws columns to table
    table = pd.merge(table, firearm_laws_database_df, on=["state", "year"], how="left")
    table.head()

    # Create new columns for each category_code
    firearm_laws_codebook_selected_columns = ["category_code", "variable_name"]
    firearm_laws_codebook_df = firearm_laws_codebook_df[
        firearm_laws_codebook_selected_columns
    ]
    category_columns = []
    for category_code in firearm_laws_codebook_df["category_code"].unique():
        category_columns.append("laws_" + str(category_code))

    for category_column in category_columns:
        table[category_column] = 0

    # Fill category columns with the corresponding value. For a state and year, check all the variables and add 1 to the corresponding category column if the value is 1
    for index, row in table.iterrows():
        for category_column in category_columns:
            for variable_name in firearm_laws_codebook_df[
                firearm_laws_codebook_df["category_code"] == int(category_column[5:])
            ]["variable_name"]:
                if row[variable_name] == 1:
                    table.at[index, category_column] += 1

    # Drop all the variables columns
    for variable_name in firearm_laws_codebook_df["variable_name"]:
        table.drop(columns=[variable_name], inplace=True)

    # Drop 'District of Columbia' and 'Hawaii' data
    table = table[~table["state"].isin(["District of Columbia", "Hawaii"])]

    # Drop data before 2015 and after 2017
    table = table[table["year"] > 2014]
    table = table[table["year"] < 2018]

    # Save table to csv
    os.makedirs("data/processed", exist_ok=True)
    table.to_csv("data/processed/incidents_combined.csv", index=False)

    return table


def create_processed_tables() -> (
    Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]
):
    """Create the processed tables.

    Returns:
        Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]: Processed tables
    """
    logging.info("Creating processed tables...")
    logging.info("Loading datasets...")
    (
        gun_violence_df,
        climate_df,
        poverty_df,
        firearm_laws_database_df,
        firearm_laws_codebook_df,
        population_df,
    ) = load_datasets()
    logging.info("Datasets loaded")

    logging.info("Selecting data...")
    (
        gun_violence_df,
        climate_df,
        firearm_laws_database_df,
        population_df,
    ) = select_data(
        gun_violence_df, climate_df, firearm_laws_database_df, population_df
    )
    logging.info("Data selected")

    logging.info("Creating incidents_weekend table...")
    incidents_weekend_table = create_incidents_weekend_table(
        gun_violence_df, population_df
    )
    logging.info("incidents_weekend table created")

    logging.info("Creating incidents_climate table...")
    incidents_climate_table = create_incidents_climate_table(
        gun_violence_df, climate_df, population_df
    )
    logging.info("incidents_climate table created")

    logging.info("Creating incidents_population_poverty table...")
    incidents_population_poverty_table = create_incidents_poverty_table(
        gun_violence_df, poverty_df, population_df
    )
    logging.info("incidents_population_poverty table created")

    logging.info("Creating incidents_firearm_laws table...")
    incidents_firearm_laws_table = create_incidents_laws_table(
        gun_violence_df,
        firearm_laws_database_df,
        firearm_laws_codebook_df,
        population_df,
    )
    logging.info("incidents_firearm_laws table created")

    logging.info("Creating incidents_combined table...")
    incidents_combined_table = create_combined_table(
        gun_violence_df,
        climate_df,
        firearm_laws_database_df,
        firearm_laws_codebook_df,
        population_df,
        poverty_df,
    )
    logging.info("incidents_combined table created")

    logging.info("All tables created")
    return (
        incidents_weekend_table,
        incidents_climate_table,
        incidents_population_poverty_table,
        incidents_firearm_laws_table,
        incidents_combined_table,
    )

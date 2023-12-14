"""
Module containing functions to preprocess the datasets,
i.e. fill null values, handle outliers, etc., creating the 'silver' layer
"""
import logging
import os
from datetime import datetime
from statistics import mean, mode
from typing import Any, List, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from parse_climate_data import parse_climate_data  # pylint: disable=import-error

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


def extract_values(column: Series) -> List[Any]:
    """Extracts values from a column with the format 'index::value|index::value|...'

    Args:
        column (Series): Column to extract values from

    Returns:
        List[Any]: List of values extracted from the column
    """
    values = []
    for row in column:
        if pd.isnull(row):
            continue
        # Remove '||' and '|' separators
        no_bars = list(filter(None, row.split("|")))
        for item in no_bars:
            if ":" in item:
                # Remove '::' and ':' separators
                no_separator = list(filter(None, item.split(":")))
                values.append(no_separator[1])
            # incident_characteristics column has a different format
            else:
                values.append(item)

    return values


def extract_values_to_lists(column: Series) -> DataFrame:
    """Extracts values from a column with the format 'index::value|index::value|...'

    Args:
        column (Series): Column to extract values from

    Returns:
        DataFrame: DataFrame with the values extracted from the column
    """
    new_column = {column.name: []}
    for row in column:
        new_row = []
        # Remove '||' and '|' separators
        no_bars = list(filter(None, row.split("|")))
        for item in no_bars:
            if ":" in item:
                # Remove '::' and ':' separators
                no_separator = list(filter(None, item.split(":")))
                if len(no_separator) == 1:
                    print("Empty value found in column", column.name)
                    new_row.append("Unknown")
                    continue
                # participant_age column has integer values
                if column.name == "participant_age":
                    new_row.append(int(no_separator[1]))
                else:
                    new_row.append(no_separator[1])
            else:
                new_row.append(item)
        new_column[column.name].append(new_row)

    return pd.DataFrame.from_dict(new_column)


def format_values(values: List[Any]) -> str:
    """Formats a list of values to the format 'index::value|index::value|...'

    Args:
        values (List[Any]): List of values to format

    Returns:
        str: Formatted values
    """
    formatted_values = ""
    n_values = len(values)
    for i in range(n_values):
        if i == n_values - 1:
            formatted_values += str(i) + "::" + str(values[i])
        else:
            formatted_values += str(i) + "::" + str(values[i]) + "||"
    return formatted_values


def impute_unknown_values(dataframe: DataFrame, columns: List[str]) -> DataFrame:
    """Imputes unknown values in the specified columns

    Args:
        dataframe (DataFrame): DataFrame to impute values
        columns (List[str]): Columns to impute values

    Returns:
        DataFrame: DataFrame with imputed values
    """
    for col in columns:
        dataframe[col].fillna("Unknown", inplace=True)

    return dataframe


def impute_mode_values(dataframe: DataFrame, columns: List[str]) -> DataFrame:
    """Imputes mode values in the specified columns

    Args:
        dataframe (DataFrame): DataFrame to impute values
        columns (List[str]): Columns to impute values

    Returns:
        DataFrame: DataFrame with imputed values
    """
    for col in columns:
        mode_value = mode(extract_values(dataframe[col]))
        dataframe[col].fillna(format_values([mode_value]), inplace=True)

    return dataframe


def impute_rounded_mean_values(dataframe: DataFrame, columns: List[str]) -> DataFrame:
    """Imputes rounded mean values in the specified columns

    Args:
        dataframe (DataFrame): DataFrame to impute values
        columns (List[str]): Columns to impute values

    Returns:
        DataFrame: DataFrame with imputed values
    """
    for col in columns:
        mean_value = dataframe[col].mean()
        mean_value = round(mean_value, 0)
        dataframe[col].fillna(mean_value, inplace=True)

    return dataframe


def impute_incidents_mean_values(dataframe: DataFrame) -> DataFrame:
    """Imputes mean values in the needed columns for the incidents dataset

    Args:
        dataframe (DataFrame): DataFrame to impute values

    Returns:
        DataFrame: DataFrame with imputed values
    """
    # 'n_guns_involved'
    n_guns_involved_mean = dataframe["n_guns_involved"].mean()
    n_guns_involved_mean = round(n_guns_involved_mean, 0)
    dataframe["n_guns_involved"].fillna(n_guns_involved_mean, inplace=True)

    # 'participant_age'
    participant_ages = extract_values(dataframe["participant_age"])
    participant_ages = [int(age) for age in participant_ages]
    participant_age_mean = mean(participant_ages)
    participant_age_mean = round(participant_age_mean, 0)
    dataframe["participant_age"].fillna(
        format_values([int(participant_age_mean)]), inplace=True
    )

    return dataframe


def impute_incidents_district_values(dataframe: DataFrame):
    """Imputes district values in the needed columns for the incidents dataset

    1. Mode for each state for `congressional_district`, `state_house_district`, `state_senate_district`
    2. -1 for `state_house_district` and `state_senate_district`

    Args:
        dataframe (DataFrame): DataFrame to impute values

    Returns:
        DataFrame: DataFrame with imputed values
    """
    # Fill null values in `congressional_district`, `state_house_district`, `state_senate_district` with the mode for the corresponding state
    states = dataframe["state"].unique()
    state_congressional_district_mode = {}
    state_house_district_mode = {}
    state_senate_district_mode = {}
    for state in states:
        state_congressional_district_mode[state] = mode(
            dataframe[dataframe["state"] == state]["congressional_district"]
        )
        state_house_district_mode[state] = mode(
            dataframe[dataframe["state"] == state]["state_house_district"]
        )
        state_senate_district_mode[state] = mode(
            dataframe[dataframe["state"] == state]["state_senate_district"]
        )

    dataframe["congressional_district"].fillna(
        dataframe["state"].map(state_congressional_district_mode), inplace=True
    )
    dataframe["state_house_district"].fillna(
        dataframe["state"].map(state_house_district_mode), inplace=True
    )
    dataframe["state_senate_district"].fillna(
        dataframe["state"].map(state_senate_district_mode), inplace=True
    )

    dataframe["state_house_district"].fillna(-1, inplace=True)
    dataframe["state_senate_district"].fillna(-1, inplace=True)

    return dataframe


def impute_incidents_location_values(dataframe: DataFrame) -> DataFrame:
    """Imputes latitude and longitude values in the needed columns for the incidents dataset with the mean for the corresponding state

    Args:
        dataframe (DataFrame): DataFrame to impute values

    Returns:
        DataFrame: DataFrame with imputed values
    """
    states = dataframe["state"].unique()
    state_latitude_mean = {}
    state_longitude_mean = {}
    for state in states:
        state_latitude_mean[state] = dataframe[dataframe["state"] == state][
            "latitude"
        ].mean()
        state_longitude_mean[state] = dataframe[dataframe["state"] == state][
            "longitude"
        ].mean()

    dataframe["latitude"].fillna(
        dataframe["state"].map(state_latitude_mean), inplace=True
    )
    dataframe["longitude"].fillna(
        dataframe["state"].map(state_longitude_mean), inplace=True
    )

    return dataframe


def fill_incidents_null_values(dataframe: DataFrame) -> DataFrame:
    """Fills null values in the needed columns for the incidents dataset

    Args:
        dataframe (DataFrame): DataFrame to impute values

    Returns:
        DataFrame: DataFrame with imputed values
    """
    # Impute unknown values
    columns_to_fill_with_unknown = [
        "participant_relationship",
        "location_description",
        "participant_name",
        "address",
        "source_url",
        "sources",
    ]
    dataframe = impute_unknown_values(dataframe, columns_to_fill_with_unknown)

    columns_to_fill_with_mode = [
        "gun_stolen",
        "gun_type",
        "participant_age_group",
        "participant_gender",
        "participant_type",
        "participant_status",
        "incident_characteristics",
    ]
    dataframe = impute_mode_values(dataframe, columns_to_fill_with_mode)

    dataframe = impute_incidents_mean_values(dataframe)
    dataframe = impute_incidents_district_values(dataframe)
    dataframe = impute_incidents_location_values(dataframe)

    dataframe["notes"].fillna("No Notes", inplace=True)

    return dataframe


def handle_incidents_outliers(dataframe: DataFrame) -> DataFrame:
    """Handles outliers in the needed columns for the incidents dataset

    Args:
        dataframe (DataFrame): DataFrame to impute values

    Returns:
        DataFrame: DataFrame with imputed values
    """
    # Extract participant ages
    participant_ages = extract_values(dataframe["participant_age"])
    participant_ages = [int(age) for age in participant_ages]
    # Identify columns to handle outliers
    numerical_columns = ["n_killed", "n_injured", "n_guns_involved"]
    numerical_data = {
        "n_killed": dataframe["n_killed"],
        "n_injured": dataframe["n_injured"],
        "n_guns_involved": dataframe["n_guns_involved"],
        "participant_age": participant_ages,
    }

    outliers = {
        "n_killed": [],
        "n_injured": [],
        "n_guns_involved": [],
        "participant_age": [],
    }

    # Calculate outliers for numerical_data as values that are 3 standard deviations away from the mean
    for col, data in numerical_data.items():
        data = np.array(data)
        mean_value = np.mean(data)
        std = np.std(data)

        threshold = 3
        col_outliers = []
        for x in data:
            z_score = (x - mean_value) / std
            if abs(z_score) > threshold:
                col_outliers.append(x)

        outliers[col] = col_outliers

    # Remove outliers from dataframe
    for col in numerical_columns:
        dataframe = dataframe[~dataframe[col].isin(outliers[col])]

    outliers["participant_age"] = [str(age) for age in outliers["participant_age"]]
    substrings_to_remove = "|".join(outliers["participant_age"])
    dataframe = dataframe[
        ~dataframe["participant_age"].str.contains(substrings_to_remove)
    ]

    return dataframe


def format_incidents_data(dataframe: DataFrame) -> DataFrame:
    """Formats the incidents dataset to a proper format

    Args:
        dataframe (DataFrame): DataFrame to impute values

    Returns:
        DataFrame: DataFrame with imputed values
    """
    columns_to_format = [
        "gun_stolen",
        "gun_type",
        "participant_age",
        "participant_age_group",
        "participant_gender",
        "participant_name",
        "participant_relationship",
        "participant_status",
        "participant_type",
    ]

    for col in columns_to_format:
        dataframe[col] = extract_values_to_lists(dataframe[col])[col].values

    # Separate date into year, month and day columns
    dataframe["year"] = pd.DatetimeIndex(  # pylint: disable=no-member
        dataframe["date"]
    ).year
    dataframe["month"] = pd.DatetimeIndex(  # pylint: disable=no-member
        dataframe["date"]
    ).month
    dataframe["day"] = pd.DatetimeIndex(  # pylint: disable=no-member
        dataframe["date"]
    ).day

    # Drop date column and reorder columns
    dataframe.drop(columns=["date"], inplace=True)
    cols = dataframe.columns.tolist()
    cols = [cols[0]] + cols[-3:] + cols[1:-3]
    dataframe = dataframe[cols]

    return dataframe


def preprocess_incidents_dataset(gun_violence_df: DataFrame) -> DataFrame:
    """Preprocesses the incidents dataset

    Args:
        gun_violence_df (DataFrame): Incidents dataset

    Returns:
        DataFrame: Preprocessed incidents dataset
    """
    # Handle null values
    logging.info("Handling incidents null values...")
    gun_violence_df = fill_incidents_null_values(gun_violence_df)
    logging.info("Incidents null values handled")

    # Handle outliers
    logging.info("Handling incidents outliers...")
    gun_violence_df = handle_incidents_outliers(gun_violence_df)
    logging.info("Incidents outliers handled")

    # Format data
    logging.info("Formatting incidents data...")
    gun_violence_df = format_incidents_data(gun_violence_df)
    logging.info("Incidents data formatted")

    # Save gun_violence_df to csv
    logging.info("Saving incidents dataset to csv...")
    os.makedirs("data/interim", exist_ok=True)
    gun_violence_df.to_csv("data/interim/gun_violence_incidents.csv", index=False)
    logging.info("Incidents dataset saved")

    return gun_violence_df


def preprocess_climate_dataset(climate_df: DataFrame) -> DataFrame:
    """Preprocesses the climate dataset

    Args:
        climate_df (DataFrame): Climate dataset

    Returns:
        DataFrame: Preprocessed climate dataset
    """
    # Handle null values
    logging.info("Handling climate null values...")
    null_columns = climate_df.columns[climate_df.isnull().any()]
    for col in null_columns:
        climate_df[col] = climate_df.groupby("state")[col].transform(
            lambda x: x.fillna(x.mean())
        )
    logging.info("Climate null values handled")

    logging.info("Formatting climate data...")
    # Convert temperature from Fahrenheit to Celsius
    climate_df["average_temperature"] = (climate_df["average_temperature"] - 32) * 5 / 9

    # Convert precipitation from inches/100 to mm
    climate_df["average_precipitation"] = climate_df["average_precipitation"] * 0.254
    logging.info("Climate data formatted")

    # Save climate_df to csv
    logging.info("Saving climate dataset to csv...")
    os.makedirs("data/interim", exist_ok=True)
    climate_df.to_csv("data/interim/climate_data.csv", index=False)
    logging.info("Climate dataset saved")

    return climate_df


def preprocess_poverty_dataset(poverty_df: DataFrame) -> DataFrame:
    """Preprocesses the poverty dataset

    Args:
        poverty_df (DataFrame): Poverty dataset

    Returns:
        DataFrame: Preprocessed poverty dataset
    """
    # Fill missing values with the mean value of the column for the corresponding state
    logging.info("Handling poverty null values...")
    null_columns = poverty_df.columns[poverty_df.isnull().any()]
    for col in null_columns:
        poverty_df[col] = poverty_df.groupby("state")[col].transform(
            lambda x: x.fillna(x.mean())
        )
    logging.info("Poverty null values handled")

    # Save poverty_df to csv
    logging.info("Saving poverty dataset to csv...")
    os.makedirs("data/interim", exist_ok=True)
    poverty_df.to_csv("data/interim/poverty_data.csv", index=False)
    logging.info("Poverty dataset saved")

    return poverty_df


def preprocess_laws_dataset(
    firearm_laws_database_df: DataFrame, firearm_laws_codebook_df: DataFrame
) -> Tuple[DataFrame, DataFrame]:
    """Preprocesses the firearm laws dataset

    Args:
        firearm_laws_database_df (DataFrame): DataFrame containing the firearm laws database
        firearm_laws_codebook_df (DataFrame): DataFrame containing the firearm laws codebook

    Returns:
        Tuple[DataFrame, DataFrame]: Preprocessed firearm laws database and codebook
    """
    # Handle null values
    logging.info("Handling firearm laws null values...")
    null_columns = firearm_laws_codebook_df.columns[
        firearm_laws_codebook_df.isnull().any()
    ]
    for col in null_columns:
        firearm_laws_codebook_df[col].fillna("Unknown", inplace=True)
    logging.info("Firearm laws null values handled")

    # Rename columns
    logging.info("Formatting firearm laws data...")
    firearm_laws_codebook_df.columns = (
        firearm_laws_codebook_df.columns.str.lower().str.replace(" ", "_")
    )
    logging.info("Firearm laws data formatted")

    # Save firearm_laws_codebook_df to csv
    logging.info("Saving firearm laws codebook to csv...")
    os.makedirs("data/interim", exist_ok=True)
    firearm_laws_codebook_df.to_csv(
        "data/interim/firearm_laws_codebook.csv", index=False
    )
    logging.info("Firearm laws codebook saved")

    # Save firearm_laws_database_df to csv
    logging.info("Saving firearm laws database to csv...")
    os.makedirs("data/interim", exist_ok=True)
    firearm_laws_database_df.to_csv(
        "data/interim/firearm_laws_database.csv", index=False
    )
    logging.info("Firearm laws database saved")

    return firearm_laws_database_df, firearm_laws_codebook_df


def create_new_population_columns(
    dataframe: DataFrame, null_columns: List[str]
) -> DataFrame:
    """Creates new columns for each year in the population dataset

    Args:
        dataframe (DataFrame): Population dataset
        null_columns (List[str]): Columns with null values for 2010

    Returns:
        DataFrame: Population dataset with new columns for each year
    """
    cols = dataframe.columns.tolist()
    # Create 'year' empty column right after 'NAME'
    cols.insert(5, "year")
    # Keep the first 5 columns
    new_population_data = {col: [] for col in cols[:5]}
    new_population_data["year"] = []
    # Extract name without year from each of the other colums
    cols_to_be_grouped = cols[8:]
    for col in cols_to_be_grouped:
        new_col = col[:-4]
        new_col = new_col.replace("_", "")
        new_population_data[new_col] = []

    # Repeat each row 10 times, one for each year
    for i in range(dataframe.shape[0]):
        # Add None values for null columns in 2010
        for col in null_columns:
            new_population_data[col].append(None)

        for j in range(10):
            new_population_data["year"].append(2010 + j)
            # For each of the old columns which end with the year, add the value to the new column
            for col in cols_to_be_grouped:
                year = int(col[-4:])
                if year == 2010 + j:
                    new_col = col[:-4]
                    new_col = new_col.replace("_", "")
                    new_population_data[new_col].append(dataframe[col][i])

            # Add the values of the first 5 columns
            for col in cols[:5]:
                new_population_data[col].append(dataframe[col][i])

    return pd.DataFrame.from_dict(new_population_data)


def fill_population_null_values(dataframe: DataFrame) -> DataFrame:
    """Imputes missing values in the population dataset

    Args:
        dataframe (DataFrame): Population dataset

    Returns:
        DataFrame: Population dataset with imputed values
    """
    null_columns = dataframe.columns[dataframe.isnull().any()]
    for col in null_columns:
        dataframe[col] = dataframe.groupby("name")[col].transform(
            lambda x: x.fillna(x.mean())
        )

    return dataframe


def preprocess_population_dataset(population_df: DataFrame) -> DataFrame:
    """Preprocesses the population dataset

    Args:
        population_df (DataFrame): Population dataset

    Returns:
        DataFrame: Preprocessed population dataset
    """
    # There are some columns with null values for 2010, which will be assigned None and handled later
    null_columns = [
        "RBIRTH",
        "RDEATH",
        "RNATURALINC",
        "RINTERNATIONALMIG",
        "RDOMESTICMIG",
        "RNETMIG",
    ]

    # Create new columns for each year
    logging.info("Formatting population data...")
    population_df = create_new_population_columns(population_df, null_columns)
    population_df.columns = population_df.columns.str.lower()
    logging.info("Population data formatted")

    # Fill null values
    logging.info("Handling population null values...")
    population_df = fill_population_null_values(population_df)
    logging.info("Population null values handled")

    # Save population_df to csv
    logging.info("Saving population dataset to csv...")
    os.makedirs("data/interim", exist_ok=True)
    population_df.to_csv("data/interim/population_data.csv", index=False)
    logging.info("Population dataset saved")

    return population_df


def load_datasets() -> (
    Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]
):
    """Loads the datasets

    Returns:
        Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]: Datasets
    """
    logging.info("Loading incidents dataset...")
    gun_violence_df = pd.read_csv("data/raw/gun-violence-data_01-2013_03-2018.csv")
    logging.info("Incidents dataset loaded")

    logging.info("Loading climate dataset...")
    climate_df = parse_climate_data(
        "data/raw/climate_state_codes.txt",
        ["data/raw/temperature_data.txt", "data/raw/precipitation_data.txt"],
    )
    logging.info("Climate dataset loaded")

    logging.info("Loading poverty dataset...")
    poverty_df = pd.read_csv("data/raw/poverty_data.csv")
    logging.info("Poverty dataset loaded")

    logging.info("Loading firearm laws dataset...")
    firearm_laws_database_df = pd.read_excel("data/raw/firearm_laws_database.xlsx")
    firearm_laws_codebook_df = pd.read_excel("data/raw/firearm_laws_codebook.xlsx")
    logging.info("Firearm laws dataset loaded")

    logging.info("Loading population dataset...")
    population_df = pd.read_csv("data/raw/population_data.csv")
    logging.info("Population dataset loaded")

    return (
        gun_violence_df,
        climate_df,
        poverty_df,
        firearm_laws_database_df,
        firearm_laws_codebook_df,
        population_df,
    )


def preprocess_datasets() -> (
    Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]
):
    """Preprocesses the datasets

    Returns:
        Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]: Preprocessed datasets
    """
    logging.info("Preprocessing datasets...")
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

    logging.info("Preprocessing incidents dataset...")
    gun_violence_df = preprocess_incidents_dataset(gun_violence_df)
    logging.info("Incidents dataset preprocessed")

    logging.info("Preprocessing climate dataset...")
    climate_df = preprocess_climate_dataset(climate_df)
    logging.info("Climate dataset preprocessed")

    logging.info("Preprocessing poverty dataset...")
    poverty_df = preprocess_poverty_dataset(poverty_df)
    logging.info("Poverty dataset preprocessed")

    logging.info("Preprocessing firearm laws dataset...")
    firearm_laws_database_df, firearm_laws_codebook_df = preprocess_laws_dataset(
        firearm_laws_database_df, firearm_laws_codebook_df
    )
    logging.info("Firearm laws dataset preprocessed")

    logging.info("Preprocessing population dataset...")
    population_df = preprocess_population_dataset(population_df)
    logging.info("Population dataset preprocessed")

    logging.info("Datasets preprocessed")
    return (
        gun_violence_df,
        climate_df,
        poverty_df,
        firearm_laws_database_df,
        firearm_laws_codebook_df,
        population_df,
    )

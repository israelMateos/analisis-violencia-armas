"""Module for parsing the climate data from the file at the given path."""
import pandas as pd
from pandas import DataFrame


def parse_state_code_table(file_path: str) -> dict:
    """Parse the state code table from the file at the given path.

    Args:
        file_path (str): Path to the file containing the state code table.

    Returns:
        dict: A dictionary mapping state codes to state names.
    """
    state_code_table = {}

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        state_code_section = False

        for line in file:
            line = line.strip()

            if line.startswith("STATE CODE TABLE:"):
                state_code_section = True
                continue

            # In the state code section, end when encountering two blank lines in a row
            if state_code_section and line:
                # Break condition
                if "110 National" in line:
                    break
                # Skip until encountering a number
                if not line[0].isdigit():
                    continue
                # Split line by whitespaces
                words = line.split()
                state_code = ""
                for word in words:
                    if word.isdigit():
                        state_code = word
                        state_code_table[state_code] = ""
                    else:
                        state_code_table[state_code] += word + " "

    # Remove whitespace at the end of state names, and state codes greater than 50
    state_codes_to_remove = []
    for state_code, state_name in state_code_table.items():
        if state_name.endswith(" "):
            state_code_table[state_code] = state_name[:-1]
        if int(state_code) > 50:
            state_codes_to_remove.append(state_code)

    for state_code in state_codes_to_remove:
        state_code_table.pop(state_code)

    # Order state codes in ascending order
    state_code_table = dict(sorted(state_code_table.items(), key=lambda item: item[0]))

    return state_code_table


def parse_climate_data(
    state_code_table_path: str, climate_data_path: str
) -> DataFrame():
    """Parse the climate data from the file at the given path.

    For each line:
     - First 3 characters are the state code
     - Characters 6-10 are the year
     - From that point on, the line is a list of 12 monthly average temperatures,
     divided by whitespaces

    Args:
        state_code_table_path (str): Path to the file containing the state code table.
        climate_data_path (str): Path to the file containing the climate data.

    Returns:
        DataFrame: A dataframe containing the climate data.
    """

    state_code_table = parse_state_code_table(state_code_table_path)

    climate_data = {
        "state": [],
        "year": [],
        "month": [],
        "average_temperature": [],
    }
    with open(climate_data_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()
            state_code = line[:3]
            year = line[6:10]
            monthly_average_temperatures = line[11:].split()

            if state_code in state_code_table:
                state_name = state_code_table[state_code]
                for month, average_temperature in enumerate(
                    monthly_average_temperatures
                ):
                    climate_data["state"].append(state_name)
                    climate_data["year"].append(int(year))
                    climate_data["month"].append(month + 1)
                    if average_temperature == "-99.90":
                        climate_data["average_temperature"].append(None)
                    else:
                        climate_data["average_temperature"].append(
                            float(average_temperature)
                        )

    climate_data = pd.DataFrame.from_dict(climate_data)
    return climate_data

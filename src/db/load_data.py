"""Functions to load raw data into the database."""
import logging
import os
import sys

sys.path.append("/app/src/data")
from datetime import datetime
from typing import Tuple

import pandas as pd
from create_processed_data import (  # pylint: disable=import-error
    create_processed_tables,
)
from preprocess_datasets import preprocess_datasets  # pylint: disable=import-error
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

# Generate a unique timestamp for the log file name
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/load_data_{timestamp}.log"

# Configure logging to write to both console and the uniquely named log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(),
    ],
)


def create_schema(session: Session, name: str) -> None:
    """Create schema in the database if it does not exist.

    Args:
        session (sqlalchemy.orm.Session): Database session.
        name (str): Name of the schema to create.
    """
    logging.info("Creating the %s schema...", name)
    try:
        session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {name}"))
        session.commit()
        logging.info("%s schema created.", name)
    except SQLAlchemyError as e:
        logging.error("Error creating schema: %s", str(e))


def add_primary_key(session: Session, schema_name: str, table_name: str) -> None:
    """Add a primary key to a table in the database.

    Args:
        session (sqlalchemy.orm.Session): Database session.
        schema_name (str): Name of the schema containing the table.
        table_name (str): Name of the table to add a primary key to.
    """
    query = (
        f"ALTER TABLE {schema_name}.{table_name} ADD COLUMN id SERIAL PRIMARY KEY"
        if table_name != "gun_violence_incidents"
        else f"ALTER TABLE {schema_name}.{table_name} ADD PRIMARY KEY (incident_id)"
    )
    logging.info("Adding primary key to %s...", table_name)
    try:
        session.execute(text(query))
        session.commit()
        logging.info("Primary key added to %s.", table_name)
    except SQLAlchemyError as e:
        logging.error("Error adding primary key: %s", str(e))


def load_data_into_database(
    engine: Engine, session: Session, schema_name: str, data_directory: str
) -> None:
    """Load data from CSV or Excel files in a specified directory into the database.

    Args:
        engine (sqlalchemy.engine.Engine): Database engine.
        session (sqlalchemy.orm.Session): Database session.
        schema_name (str): Name of the schema to load data into.
        data_directory (str): Path to the directory containing data files.
    """
    files = [f for f in os.listdir(data_directory) if f.endswith((".csv", ".xlsx"))]

    for file in files:
        file_path = os.path.join(data_directory, file)
        table_name = os.path.splitext(file)[0]

        if table_name == "gun-violence-data_01-2013_03-2018":
            table_name = "gun_violence_incidents"

        df = (
            pd.read_excel(file_path)
            if file.endswith(".xlsx")
            else pd.read_csv(file_path)
        )

        logging.info("Loading %s into the database...", file_path)
        df.to_sql(
            table_name, engine, schema=schema_name, if_exists="replace", index=False
        )
        add_primary_key(session, schema_name, table_name)
        logging.info("%s loaded into the database.", file_path)


def create_connection() -> Tuple[Engine, Session]:
    """Create a connection to the database.

    Returns:
        Tuple[Engine, Session]: Database engine and session.
    """
    postgres_host = os.environ.get("POSTGRES_HOST")
    postgres_port = os.environ.get("POSTGRES_PORT")
    postgres_db = os.environ.get("POSTGRES_DB")
    postgres_user = os.environ.get("POSTGRES_USER")
    postgres_password = os.environ.get("POSTGRES_PASSWORD")

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=postgres_user,
        password=postgres_password,
        host=postgres_host,
        port=postgres_port,
        database=postgres_db,
    )
    logging.info("Creating engine...")
    engine = create_engine(url)
    logging.info("Engine created.")

    logging.info("Creating session...")
    session = sessionmaker(bind=engine)()
    logging.info("Session created.")

    return engine, session


def main() -> None:
    """Main function to load all data into the database."""
    engine, session = create_connection()

    logging.info("Loading data into the database...")
    logging.info("Loading raw data into the database...")
    create_schema(session, "raw")
    load_data_into_database(engine, session, "raw", "/app/data/raw")
    logging.info("Raw data loaded into the database.")

    preprocess_datasets()
    logging.info("Loading silver data into the database...")
    create_schema(session, "silver")
    load_data_into_database(engine, session, "silver", "/app/data/interim")
    logging.info("silver data loaded into the database.")

    create_processed_tables()
    logging.info("Loading gold data into the database...")
    create_schema(session, "gold")
    load_data_into_database(engine, session, "gold", "/app/data/processed")
    logging.info("gold data loaded into the database.")

    logging.info("Data loaded into the database.")


if __name__ == "__main__":
    main()

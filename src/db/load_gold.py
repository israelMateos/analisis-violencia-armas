"""Functions to load gold data into the database."""
import logging
import os
from datetime import datetime
import sys
sys.path.append('/app/src/data')

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from create_processed_data import create_processed_tables  # pylint: disable=import-error

# Generate a unique timestamp for the log file name
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/load_gold_{timestamp}.log"

# Configure logging to write to both console and the uniquely named log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(),
    ],
)


def create_gold_schema(session: Session) -> None:
    """Create the 'gold' schema in the database if it does not exist.

    Args:
        session (sqlalchemy.orm.Session): Database session.
    """
    logging.info("Creating the gold schema...")
    try:
        session.execute(text("CREATE SCHEMA IF NOT EXISTS gold"))
        session.commit()
        logging.info("gold schema created.")
    except SQLAlchemyError as e:
        logging.error("Error creating schema: %s", str(e))


def load_data_into_database(engine: Engine, data_directory: str) -> None:
    """Load data from CSV files in a specified directory into the database.

    Args:
        engine (sqlalchemy.engine.Engine): Database engine.
        data_directory (str): Path to the directory containing data files.
    """
    files = [f for f in os.listdir(data_directory) if f.endswith(".csv")]

    for file in files:
        file_path = os.path.join(data_directory, file)
        table_name = os.path.splitext(file)[0]

        df = pd.read_csv(file_path)
        logging.info("Loading %s into the database...", file_path)
        df.to_sql(table_name, engine, schema="gold", if_exists="replace", index=False)
        logging.info("%s loaded into the database.", file_path)


def main() -> None:
    """Main function to load data into the database."""
    logging.info("Loading data into the database...")
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

    logging.info("Preprocessing datasets...")
    create_processed_tables()
    logging.info("Datasets preprocessed.")

    logging.info("Creating engine...")
    engine = create_engine(url)
    logging.info("Engine created.")

    logging.info("Creating session...")
    session = sessionmaker(bind=engine)()
    logging.info("Session created.")

    create_gold_schema(session)

    data_directory = "/app/data/processed"

    logging.info("Loading data into the database...")
    load_data_into_database(engine, data_directory)
    logging.info("Data loaded into the database.")

    sys.exit(0)


if __name__ == "__main__":
    main()

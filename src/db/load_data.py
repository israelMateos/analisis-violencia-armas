import logging
import os

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_raw_schema(session):
    logging.info("Creating the raw schema...")
    try:
        session.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
        session.commit()
        logging.info("Raw schema created.")
    except Exception as e:
        logging.error("Error creating schema: %s", str(e))


def load_data_into_database(engine, data_directory):
    files = [f for f in os.listdir(data_directory) if f.endswith((".csv", ".xlsx"))]

    for file in files:
        file_path = os.path.join(data_directory, file)
        table_name = os.path.splitext(file)[0]

        df = (
            pd.read_excel(file_path)
            if file.endswith(".xlsx")
            else pd.read_csv(file_path)
        )
        logging.info("Loading %s into the database...", file_path)
        df.to_sql(table_name, engine, schema="raw", if_exists="replace", index=False)
        logging.info("%s loaded into the database.", file_path)


def main():
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
    logging.info("Creating engine...")
    engine = create_engine(url)
    logging.info("Engine created.")

    logging.info("Creating session...")
    session = sessionmaker(bind=engine)()
    logging.info("Session created.")

    create_raw_schema(session)

    data_directory = "/app/data/raw"

    logging.info("Loading data into the database...")
    load_data_into_database(engine, data_directory)
    logging.info("Data loaded into the database.")


if __name__ == "__main__":
    main()

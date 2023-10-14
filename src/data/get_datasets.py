from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
import kaggle


def get_gun_violence_data():
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(
        "jameslko/gun-violence-data", path="data/raw", unzip=True
    )


def get_datasets():
    get_gun_violence_data()

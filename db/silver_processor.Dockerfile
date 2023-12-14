FROM python:3.9-alpine3.13

WORKDIR /app

COPY requirements/containers/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/data/__init__.py /app/src/data/__init__.py
COPY ./src/data/parse_climate_data.py /app/src/data/parse_climate_data.py
COPY ./src/data/preprocess_datasets.py /app/src/data/preprocess_datasets.py
COPY ./src/db/process_silver.py /app/src/db/process_silver.py

CMD [ "python3", "./src/db/process_silver.py" ]

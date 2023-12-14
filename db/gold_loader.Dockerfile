FROM python:3.9-alpine3.13

WORKDIR /app

COPY requirements/containers/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/data/__init__.py /app/src/data/__init__.py
COPY ./src/data/create_processed_data.py /app/src/data/create_processed_data.py
COPY ./src/db/load_gold.py /app/src/db/load_gold.py

CMD [ "python3", "./src/db/load_gold.py" ]

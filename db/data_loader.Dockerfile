FROM python:3.9-alpine3.13

WORKDIR /app

COPY requirements/containers/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/db/load_data.py /app/src/db/load_data.py
COPY ./data/raw /app/data/raw

CMD [ "python3", "./src/db/load_data.py" ]

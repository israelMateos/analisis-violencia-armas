FROM python:3.9-alpine3.13

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/db /app/src/db
COPY ./data/raw /app/data/raw

CMD [ "python3", "./src/db/load_data.py" ]

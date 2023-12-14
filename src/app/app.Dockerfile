# FastAPI app

FROM python:3.9-alpine

WORKDIR /app

COPY requirements/app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/app /app/src/app

CMD [ "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
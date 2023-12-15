# FastAPI app

FROM python:3.9-alpine

WORKDIR /app

COPY requirements/app/backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/app/backend /app/src/app/backend

CMD [ "uvicorn", "src.app.backend.main:app", "--host", "0.0.0.0", "--port", "8000" ]
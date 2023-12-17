# FastAPI app

FROM python:3.10-alpine

WORKDIR /app

COPY requirements/backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/app/backend /app/src/app/backend

EXPOSE 8000

CMD [ "uvicorn", "src.app.backend.main:app", "--host", "0.0.0.0", "--port", "8000" ]
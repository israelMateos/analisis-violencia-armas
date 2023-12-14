import sys
import logging

sys.path.append("src/app")
from fastapi import FastAPI

import models  # pylint: disable=import-error
from db import engine  # pylint: disable=import-error
from api import incidents_weekend  # pylint: disable=import-error


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(incidents_weekend.router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello World"}
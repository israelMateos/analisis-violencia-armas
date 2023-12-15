import logging
import sys

sys.path.append("src/app/backend")
import models  # pylint: disable=import-error
from api import (  # pylint: disable=import-error
    incidents_climate,
    incidents_combined,
    incidents_firearm_laws,
    incidents_population_poverty,
    incidents_weekend,
)
from fastapi import FastAPI

from db import engine  # pylint: disable=import-error

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(incidents_weekend.router)
app.include_router(incidents_climate.router)
app.include_router(incidents_population_poverty.router)
app.include_router(incidents_firearm_laws.router)
app.include_router(incidents_combined.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello World"}

"""API endpoints for incidents_climate."""
import sys

sys.path.append("src/app")
from crud.crud_incidents_climate import (  # pylint: disable=import-error
    CRUDIncidentsClimate,
)
from fastapi import APIRouter, Depends, HTTPException
from models import IncidentClimate  # pylint: disable=import-error
from sqlalchemy.orm import Session

from db import get_db  # pylint: disable=import-error

router = APIRouter()


@router.get("/incidents/climate/", response_model=None)
async def get_incidents_climate(db: Session = Depends(get_db)):
    """Get all incidents_climate."""
    return CRUDIncidentsClimate(IncidentClimate).get_multi(db)


# Get incidents_climate by id
@router.get("/incidents/climate/{id}", response_model=None)
async def get_incidents_climate_by_id(id: int, db: Session = Depends(get_db)):
    """Get all incidents_climate by id."""
    incidents_climate = CRUDIncidentsClimate(IncidentClimate).get(db, id=id)
    if not incidents_climate:
        raise HTTPException(status_code=404, detail="Incidents_climate not found")
    return incidents_climate


# Get incidents_climate by state
@router.get("/incidents/climate/{state}", response_model=None)
async def get_incidents_climate_by_state(state: str, db: Session = Depends(get_db)):
    """Get all incidents_climate by state."""
    incidents_climate = CRUDIncidentsClimate(IncidentClimate).get_multi_by_state(
        db, state=state
    )
    if not incidents_climate:
        raise HTTPException(status_code=404, detail="Incidents_climate not found")
    return incidents_climate


# Get incidents_climate by year
@router.get("/incidents/climate/{year}", response_model=None)
async def get_incidents_climate_by_year(state: str, db: Session = Depends(get_db)):
    """Get all incidents_climate by year."""
    incidents_climate = CRUDIncidentsClimate(IncidentClimate).get_multi_by_year(
        db, state=state
    )
    if not incidents_climate:
        raise HTTPException(status_code=404, detail="Incidents_climate not found")
    return incidents_climate

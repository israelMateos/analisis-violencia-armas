"""API endpoints for incidents_climate."""
import sys

sys.path.append("src/app/backend")
from crud.crud_incidents_climate import (  # pylint: disable=import-error
    CRUDIncidentsClimate,
)
from fastapi import APIRouter, Depends, HTTPException
from models import IncidentClimate  # pylint: disable=import-error
from schemas import (  # pylint: disable=import-error
    IncidentClimateCreate,
    IncidentClimateUpdate,
)
from sqlalchemy.orm import Session

from db import get_db  # pylint: disable=import-error

router = APIRouter()


# Get incidents_climate by id
@router.get("/incidents/climate/{id}", response_model=None)
async def get_incidents_climate_by_id(id: int, db: Session = Depends(get_db)):
    """Get all incidents_climate by id."""
    incidents_climate = CRUDIncidentsClimate(IncidentClimate).get(db, id=id)
    if not incidents_climate:
        raise HTTPException(status_code=404, detail="Incidents_climate not found")
    return incidents_climate


# Get incidents_climate by state and/or year
@router.get("/incidents/climate/", response_model=None)
async def get_incidents_climate(
    state: str | None = None,
    year: int | None = None,
    db: Session = Depends(get_db)
):
    """Get all incidents_climate by state and/or year."""
    if state and year:
        incidents_climate = CRUDIncidentsClimate(
            IncidentClimate
        ).get_multi_by_state_and_year(db, state=state, year=year)
    elif state:
        incidents_climate = CRUDIncidentsClimate(
            IncidentClimate
        ).get_multi_by_state(db, state=state)
    elif year:
        incidents_climate = CRUDIncidentsClimate(
            IncidentClimate
        ).get_multi_by_year(db, year=year)
    else:
        incidents_climate = CRUDIncidentsClimate(IncidentClimate).get_multi(db)
    if not incidents_climate:
        raise HTTPException(status_code=404, detail="Incidents_climate not found")
    return incidents_climate


# Create incidents_climate
@router.post("/incidents/climate/")
async def create_incidents_climate(
    incidents_climate: IncidentClimateCreate, db: Session = Depends(get_db)
):
    """Create incidents_climate."""
    return CRUDIncidentsClimate(IncidentClimate).create(db, obj_in=incidents_climate)


# Update incidents_climate
@router.put("/incidents/climate/{id}")
async def update_incidents_climate(
    id: int, incidents_climate: IncidentClimateUpdate, db: Session = Depends(get_db)
):
    """Update incidents_climate."""
    db_obj = CRUDIncidentsClimate(IncidentClimate).get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Incidents_climate not found")
    return CRUDIncidentsClimate(IncidentClimate).update(
        db, db_obj=db_obj, obj_in=incidents_climate
    )


# Delete incidents_climate
@router.delete("/incidents/climate/{id}")
async def delete_incidents_climate(id: int, db: Session = Depends(get_db)):
    """Delete incidents_climate."""
    db_incidents_climate = CRUDIncidentsClimate(IncidentClimate).get(db, id=id)
    if not db_incidents_climate:
        raise HTTPException(status_code=404, detail="Incidents_climate not found")
    return CRUDIncidentsClimate(IncidentClimate).remove(db, id=db_incidents_climate.id)

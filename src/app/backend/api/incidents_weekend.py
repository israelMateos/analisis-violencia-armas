"""API endpoints for incidents_weekend."""
import sys

sys.path.append("src/app/backend")
from crud.crud_incidents_weekend import (  # pylint: disable=import-error
    CRUDIncidentsWeekend,
)
from fastapi import APIRouter, Depends, HTTPException
from models import IncidentWeekend  # pylint: disable=import-error
from sqlalchemy.orm import Session

from db import get_db  # pylint: disable=import-error

router = APIRouter()


@router.get("/incidents/weekend/", response_model=None)
async def get_incidents_weekend(db: Session = Depends(get_db)):
    """Get all incidents_weekend."""
    return CRUDIncidentsWeekend(IncidentWeekend).get_multi(db)


# Get incidents_weekend by id
@router.get("/incidents/weekend/{id}", response_model=None)
async def get_incidents_weekend_by_id(id: int, db: Session = Depends(get_db)):
    """Get all incidents_weekend by id."""
    incidents_weekend = CRUDIncidentsWeekend(IncidentWeekend).get(db, id=id)
    if not incidents_weekend:
        raise HTTPException(status_code=404, detail="Incidents_weekend not found")
    return incidents_weekend


# Get incidents_weekend by state
@router.get("/incidents/weekend/{state}", response_model=None)
async def get_incidents_weekend_by_state(state: str, db: Session = Depends(get_db)):
    """Get all incidents_weekend by state."""
    incidents_weekend = CRUDIncidentsWeekend(IncidentWeekend).get_multi_by_state(
        db, state=state
    )
    if not incidents_weekend:
        raise HTTPException(status_code=404, detail="Incidents_weekend not found")
    return incidents_weekend


# Get incidents_weekend by year
@router.get("/incidents/weekend/{year}", response_model=None)
async def get_incidents_weekend_by_year(state: str, db: Session = Depends(get_db)):
    """Get all incidents_weekend by year."""
    incidents_weekend = CRUDIncidentsWeekend(IncidentWeekend).get_multi_by_year(
        db, state=state
    )
    if not incidents_weekend:
        raise HTTPException(status_code=404, detail="Incidents_weekend not found")
    return incidents_weekend

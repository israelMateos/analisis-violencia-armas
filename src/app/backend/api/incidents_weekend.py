"""API endpoints for incidents_weekend."""
import sys

sys.path.append("src/app/backend")
from crud.crud_incidents_weekend import (  # pylint: disable=import-error
    CRUDIncidentsWeekend,
)
from fastapi import APIRouter, Depends, HTTPException
from models import IncidentWeekend  # pylint: disable=import-error
from schemas import IncidentWeekendCreate  # pylint: disable=import-error
from sqlalchemy.orm import Session

from db import get_db  # pylint: disable=import-error

router = APIRouter()


@router.get("/incidents/weekend/")
async def get_incidents_weekend(db: Session = Depends(get_db)):
    """Get all incidents_weekend."""
    return CRUDIncidentsWeekend(IncidentWeekend).get_multi(db)


# Get incidents_weekend by id
@router.get("/incidents/weekend/{id}")
async def get_incidents_weekend_by_id(id: int, db: Session = Depends(get_db)):
    """Get all incidents_weekend by id."""
    incidents_weekend = CRUDIncidentsWeekend(IncidentWeekend).get(db, id=id)
    if not incidents_weekend:
        raise HTTPException(status_code=404, detail="Incidents_weekend not found")
    return incidents_weekend


# Get incidents_weekend by state
@router.get("/incidents/weekend/{state}")
async def get_incidents_weekend_by_state(state: str, db: Session = Depends(get_db)):
    """Get all incidents_weekend by state."""
    incidents_weekend = CRUDIncidentsWeekend(IncidentWeekend).get_multi_by_state(
        db, state=state
    )
    if not incidents_weekend:
        raise HTTPException(status_code=404, detail="Incidents_weekend not found")
    return incidents_weekend


# Get incidents_weekend by year
@router.get("/incidents/weekend/{year}")
async def get_incidents_weekend_by_year(state: str, db: Session = Depends(get_db)):
    """Get all incidents_weekend by year."""
    incidents_weekend = CRUDIncidentsWeekend(IncidentWeekend).get_multi_by_year(
        db, state=state
    )
    if not incidents_weekend:
        raise HTTPException(status_code=404, detail="Incidents_weekend not found")
    return incidents_weekend

# Create incidents_weekend
@router.post("/incidents/weekend/")
async def create_incidents_weekend(
    incidents_weekend: IncidentWeekendCreate, db: Session = Depends(get_db)
):
    """Create incidents_weekend."""
    return CRUDIncidentsWeekend(IncidentWeekendCreate).create(db, obj_in=incidents_weekend)

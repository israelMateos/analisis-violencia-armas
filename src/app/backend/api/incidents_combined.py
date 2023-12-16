"""API endpoints for incidents_combined."""
import sys

sys.path.append("src/app/backend")
from crud.crud_incidents_combined import (  # pylint: disable=import-error
    CRUDIncidentsCombined,
)
from fastapi import APIRouter, Depends, HTTPException
from models import IncidentCombined  # pylint: disable=import-error
from schemas import IncidentCombinedCreate  # pylint: disable=import-error
from sqlalchemy.orm import Session

from db import get_db  # pylint: disable=import-error

router = APIRouter()


@router.get("/incidents/combined/", response_model=None)
async def get_incidents_combined(db: Session = Depends(get_db)):
    """Get all incidents_combined."""
    return CRUDIncidentsCombined(IncidentCombined).get_multi(db)


# Get incidents_combined by id
@router.get("/incidents/combined/{id}", response_model=None)
async def get_incidents_combined_by_id(id: int, db: Session = Depends(get_db)):
    """Get all incidents_combined by id."""
    incidents_combined = CRUDIncidentsCombined(IncidentCombined).get(db, id=id)
    if not incidents_combined:
        raise HTTPException(status_code=404, detail="Incidents_combined not found")
    return incidents_combined


# Get incidents_combined by state
@router.get("/incidents/combined/{state}", response_model=None)
async def get_incidents_combined_by_state(state: str, db: Session = Depends(get_db)):
    """Get all incidents_combined by state."""
    incidents_combined = CRUDIncidentsCombined(IncidentCombined).get_multi_by_state(
        db, state=state
    )
    if not incidents_combined:
        raise HTTPException(status_code=404, detail="Incidents_combined not found")
    return incidents_combined


# Get incidents_combined by year
@router.get("/incidents/combined/{year}", response_model=None)
async def get_incidents_combined_by_year(state: str, db: Session = Depends(get_db)):
    """Get all incidents_combined by year."""
    incidents_combined = CRUDIncidentsCombined(IncidentCombined).get_multi_by_year(
        db, state=state
    )
    if not incidents_combined:
        raise HTTPException(status_code=404, detail="Incidents_combined not found")
    return incidents_combined

# Create incidents_combined
@router.post("/incidents/combined/")
async def create_incidents_combined(
    incidents_combined: IncidentCombinedCreate, db: Session = Depends(get_db)
):
    """Create incidents_combined."""
    return CRUDIncidentsCombined(IncidentCombined).create(db, obj_in=incidents_combined)
"""API endpoints for incidents_combined."""
import sys

sys.path.append("src/app/backend")
from crud.crud_incidents_combined import (  # pylint: disable=import-error
    CRUDIncidentsCombined,
)
from fastapi import APIRouter, Depends, HTTPException
from models import IncidentCombined  # pylint: disable=import-error
from schemas import (  # pylint: disable=import-error
    IncidentCombinedCreate,
    IncidentCombinedUpdate,
)
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


# Get incidents_combined by state and/or year
@router.get("/incidents/combined/", response_model=None)
async def get_incidents_combined(
    state: str | None = None,
    year: int | None = None,
    db: Session = Depends(get_db)
):
    """Get all incidents_combined by state and/or year."""
    if state and year:
        incidents_combined = CRUDIncidentsCombined(
            IncidentCombined
        ).get_multi_by_state_and_year(db, state=state, year=year)
    elif state:
        incidents_combined = CRUDIncidentsCombined(
            IncidentCombined
        ).get_multi_by_state(db, state=state)
    elif year:
        incidents_combined = CRUDIncidentsCombined(
            IncidentCombined
        ).get_multi_by_year(db, year=year)
    else:
        incidents_combined = CRUDIncidentsCombined(IncidentCombined).get_multi(db)
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


# Update incidents_combined
@router.put("/incidents/combined/{id}")
async def update_incidents_combined(
    id: int, incidents_combined: IncidentCombinedUpdate, db: Session = Depends(get_db)
):
    """Update incidents_combined."""
    db_obj = CRUDIncidentsCombined(IncidentCombined).get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Incidents_combined not found")
    return CRUDIncidentsCombined(IncidentCombined).update(
        db, db_obj=db_obj, obj_in=incidents_combined
    )


# Delete incidents_combined
@router.delete("/incidents/combined/{id}")
async def delete_incidents_combined(id: int, db: Session = Depends(get_db)):
    """Delete incidents_combined."""
    db_incidents_combined = CRUDIncidentsCombined(IncidentCombined).get(db, id=id)
    if not db_incidents_combined:
        raise HTTPException(status_code=404, detail="Incidents_combined not found")
    return CRUDIncidentsCombined(IncidentCombined).remove(db, id=db_incidents_combined.id)

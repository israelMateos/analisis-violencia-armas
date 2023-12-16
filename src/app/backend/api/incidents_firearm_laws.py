"""API endpoints for incidents_firearm_laws."""
import sys

sys.path.append("src/app/backend")
from crud.crud_incidents_firearm_laws import (  # pylint: disable=import-error
    CRUDIncidentsFirearmLaws,
)
from fastapi import APIRouter, Depends, HTTPException
from models import IncidentFirearmLaws  # pylint: disable=import-error
from schemas import (  # pylint: disable=import-error
    IncidentFirearmLawsCreate,
    IncidentFirearmLawsUpdate,
)
from sqlalchemy.orm import Session

from db import get_db  # pylint: disable=import-error

router = APIRouter()


# Get incidents_firearm_laws by id
@router.get("/incidents/firearm_laws/{id}", response_model=None)
async def get_incidents_firearm_laws_by_id(id: int, db: Session = Depends(get_db)):
    """Get all incidents_firearm_laws by id."""
    incidents_firearm_laws = CRUDIncidentsFirearmLaws(IncidentFirearmLaws).get(
        db, id=id
    )
    if not incidents_firearm_laws:
        raise HTTPException(status_code=404, detail="Incidents_firearm_laws not found")
    return incidents_firearm_laws


# Get incidents_firearm_laws by state and/or year
@router.get("/incidents/firearm_laws/", response_model=None)
async def get_incidents_firearm_laws(
    state: str | None = None,
    year: int | None = None,
    db: Session = Depends(get_db)
):
    """Get all incidents_firearm_laws by state and/or year."""
    if state and year:
        incidents_firearm_laws = CRUDIncidentsFirearmLaws(
            IncidentFirearmLaws
        ).get_multi_by_state_and_year(db, state=state, year=year)
    elif state:
        incidents_firearm_laws = CRUDIncidentsFirearmLaws(
            IncidentFirearmLaws
        ).get_multi_by_state(db, state=state)
    elif year:
        incidents_firearm_laws = CRUDIncidentsFirearmLaws(
            IncidentFirearmLaws
        ).get_multi_by_year(db, year=year)
    else:
        incidents_firearm_laws = CRUDIncidentsFirearmLaws(IncidentFirearmLaws).get_multi(db)
    if not incidents_firearm_laws:
        raise HTTPException(status_code=404, detail="Incidents_firearm_laws not found")
    return incidents_firearm_laws


# Create incidents_firearm_laws
@router.post("/incidents/firearm_laws/")
async def create_incidents_firearm_laws(
    incidents_firearm_laws: IncidentFirearmLawsCreate, db: Session = Depends(get_db)
):
    """Create incidents_firearm_laws."""
    return CRUDIncidentsFirearmLaws(IncidentFirearmLaws).create(
        db, obj_in=incidents_firearm_laws
    )


# Update incidents_firearm_laws
@router.put("/incidents/firearm_laws/{id}")
async def update_incidents_firearm_laws(
    id: int,
    incidents_firearm_laws: IncidentFirearmLawsUpdate,
    db: Session = Depends(get_db),
):
    """Update incidents_firearm_laws."""
    db_incidents_firearm_laws = CRUDIncidentsFirearmLaws(IncidentFirearmLaws).get(
        db, id=id
    )
    if not db_incidents_firearm_laws:
        raise HTTPException(status_code=404, detail="Incidents_firearm_laws not found")
    return CRUDIncidentsFirearmLaws(IncidentFirearmLaws).update(
        db, db_obj=db_incidents_firearm_laws, obj_in=incidents_firearm_laws
    )


# Delete incidents_firearm_laws
@router.delete("/incidents/firearm_laws/{id}")
async def delete_incidents_firearm_laws(id: int, db: Session = Depends(get_db)):
    """Delete incidents_firearm_laws."""
    db_incidents_firearm_laws = CRUDIncidentsFirearmLaws(IncidentFirearmLaws).get(
        db, id=id
    )
    if not db_incidents_firearm_laws:
        raise HTTPException(status_code=404, detail="Incidents_firearm_laws not found")
    return CRUDIncidentsFirearmLaws(IncidentFirearmLaws).remove(db, id=db_incidents_firearm_laws.id)

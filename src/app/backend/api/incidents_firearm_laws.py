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


@router.get("/incidents/firearm_laws/", response_model=None)
async def get_incidents_firearm_laws(db: Session = Depends(get_db)):
    """Get all incidents_firearm_laws."""
    return CRUDIncidentsFirearmLaws(IncidentFirearmLaws).get_multi(db)


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


# Get incidents_firearm_laws by state
@router.get("/incidents/firearm_laws/{state}", response_model=None)
async def get_incidents_firearm_laws_by_state(
    state: str, db: Session = Depends(get_db)
):
    """Get all incidents_firearm_laws by state."""
    incidents_firearm_laws = CRUDIncidentsFirearmLaws(
        IncidentFirearmLaws
    ).get_multi_by_state(db, state=state)
    if not incidents_firearm_laws:
        raise HTTPException(status_code=404, detail="Incidents_firearm_laws not found")
    return incidents_firearm_laws


# Get incidents_firearm_laws by year
@router.get("/incidents/firearm_laws/{year}", response_model=None)
async def get_incidents_firearm_laws_by_year(state: str, db: Session = Depends(get_db)):
    """Get all incidents_firearm_laws by year."""
    incidents_firearm_laws = CRUDIncidentsFirearmLaws(
        IncidentFirearmLaws
    ).get_multi_by_year(db, state=state)
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

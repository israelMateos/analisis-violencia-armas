"""API endpoints for incidents_population_poverty."""
import sys

sys.path.append("src/app/backend")
from crud.crud_incidents_population_poverty import (  # pylint: disable=import-error
    CRUDIncidentsPopulationPoverty,
)
from fastapi import APIRouter, Depends, HTTPException
from models import IncidentPopulationPoverty  # pylint: disable=import-error
from schemas import (  # pylint: disable=import-error
    IncidentPopulationPovertyCreate,
    IncidentPopulationPovertyUpdate,
)
from sqlalchemy.orm import Session

from db import get_db  # pylint: disable=import-error

router = APIRouter()


@router.get("/incidents/population_poverty/", response_model=None)
async def get_incidents_population_poverty(db: Session = Depends(get_db)):
    """Get all incidents_population_poverty."""
    return CRUDIncidentsPopulationPoverty(IncidentPopulationPoverty).get_multi(db)


# Get incidents_population_poverty by id
@router.get("/incidents/population_poverty/{id}", response_model=None)
async def get_incidents_population_poverty_by_id(
    id: int, db: Session = Depends(get_db)
):
    """Get all incidents_population_poverty by id."""
    incidents_population_poverty = CRUDIncidentsPopulationPoverty(
        IncidentPopulationPoverty
    ).get(db, id=id)
    if not incidents_population_poverty:
        raise HTTPException(
            status_code=404, detail="Incidents_population_poverty not found"
        )
    return incidents_population_poverty


# Get incidents_population_poverty by state
@router.get("/incidents/population_poverty/{state}", response_model=None)
async def get_incidents_population_poverty_by_state(
    state: str, db: Session = Depends(get_db)
):
    """Get all incidents_population_poverty by state."""
    incidents_population_poverty = CRUDIncidentsPopulationPoverty(
        IncidentPopulationPoverty
    ).get_multi_by_state(db, state=state)
    if not incidents_population_poverty:
        raise HTTPException(
            status_code=404, detail="Incidents_population_poverty not found"
        )
    return incidents_population_poverty


# Get incidents_population_poverty by year
@router.get("/incidents/population_poverty/{year}", response_model=None)
async def get_incidents_population_poverty_by_year(
    state: str, db: Session = Depends(get_db)
):
    """Get all incidents_population_poverty by year."""
    incidents_population_poverty = CRUDIncidentsPopulationPoverty(
        IncidentPopulationPoverty
    ).get_multi_by_year(db, state=state)
    if not incidents_population_poverty:
        raise HTTPException(
            status_code=404, detail="Incidents_population_poverty not found"
        )
    return incidents_population_poverty


# Get incidents_population_poverty by state and year
@router.get("/incidents/population_poverty/{state}/{year}", response_model=None)
async def get_incidents_population_poverty_by_state_and_year(
    state: str, year: int, db: Session = Depends(get_db)
):
    """Get all incidents_population_poverty by state and year."""
    incidents_population_poverty = CRUDIncidentsPopulationPoverty(
        IncidentPopulationPoverty
    ).get_multi_by_state_and_year(db, state=state, year=year)
    if not incidents_population_poverty:
        raise HTTPException(
            status_code=404, detail="Incidents_population_poverty not found"
        )
    return incidents_population_poverty


# Create incidents_population_poverty
@router.post("/incidents/population_poverty/")
async def create_incidents_population_poverty(
    incidents_population_poverty: IncidentPopulationPovertyCreate,
    db: Session = Depends(get_db),
):
    """Create incidents_population_poverty."""
    return CRUDIncidentsPopulationPoverty(IncidentPopulationPoverty).create(
        db, obj_in=incidents_population_poverty
    )


# Update incidents_population_poverty
@router.put("/incidents/population_poverty/{id}")
async def update_incidents_population_poverty(
    id: int,
    incidents_population_poverty: IncidentPopulationPovertyUpdate,
    db: Session = Depends(get_db),
):
    """Update incidents_population_poverty."""
    db_incidents_population_poverty = CRUDIncidentsPopulationPoverty(
        IncidentPopulationPoverty
    ).get(db, id=id)
    if not db_incidents_population_poverty:
        raise HTTPException(
            status_code=404, detail="Incidents_population_poverty not found"
        )
    return CRUDIncidentsPopulationPoverty(IncidentPopulationPoverty).update(
        db, db_obj=db_incidents_population_poverty, obj_in=incidents_population_poverty
    )


# Delete incidents_population_poverty
@router.delete("/incidents/population_poverty/{id}")
async def remove_incidents_population_poverty(id: int, db: Session = Depends(get_db)):
    """Delete incidents_population_poverty."""
    db_incidents_population_poverty = CRUDIncidentsPopulationPoverty(
        IncidentPopulationPoverty
    ).get(db, id=id)
    if not db_incidents_population_poverty:
        raise HTTPException(
            status_code=404, detail="Incidents_population_poverty not found"
        )
    return CRUDIncidentsPopulationPoverty(IncidentPopulationPoverty).remove(
        db, id=db_incidents_population_poverty.id
    )

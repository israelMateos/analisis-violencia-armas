"""API endpoints for incidents_population_poverty."""
import sys

sys.path.append("src/app")
from crud.crud_incidents_population_poverty import (  # pylint: disable=import-error
    CRUDIncidentsPopulationPoverty,
)
from fastapi import APIRouter, Depends, HTTPException
from models import IncidentPopulationPoverty  # pylint: disable=import-error
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

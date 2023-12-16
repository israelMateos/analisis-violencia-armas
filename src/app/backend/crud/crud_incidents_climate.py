"""CRUDIncidentsClimate module."""
import sys

from src.app.backend.schemas.incident_climate import IncidentClimateCreate

sys.path.append("src/app/backend")
from typing import Optional

from crud.base import CRUDBase  # pylint: disable=import-error
from models import IncidentClimate  # pylint: disable=import-error
from schemas import (  # pylint: disable=import-error
    IncidentClimateCreate,
    IncidentClimateUpdate,
)
from sqlalchemy.orm import Session


class CRUDIncidentsClimate(
    CRUDBase[IncidentClimate, IncidentClimateCreate, IncidentClimateUpdate]
):
    # GET
    def get(self, db: Session, *, id: int) -> Optional[IncidentClimate]:
        """Get incidents_climate by id."""
        return super().get(db, id=id)

    def get_multi(self, db: Session) -> Optional[IncidentClimate]:
        """Get all incidents_climate."""
        return db.query(self.model).all()

    def get_multi_by_state(
        self, db: Session, *, state: str
    ) -> Optional[IncidentClimate]:
        """Get all incidents_climate by state."""
        return db.query(self.model).filter(self.model.state == state).all()

    def get_multi_by_year(self, db: Session, *, year: int) -> Optional[IncidentClimate]:
        """Get all incidents_climate by year."""
        return db.query(self.model).filter(self.model.year == year).all()

    def get_multi_by_state_and_year(
        self, db: Session, *, state: str, year: int
    ) -> Optional[IncidentClimate]:
        """Get all incidents_climate by state and year."""
        return (
            db.query(self.model)
            .filter(self.model.state == state, self.model.year == year)
            .all()
        )

    # POST
    def create(self, db: Session, *, obj_in: IncidentClimateCreate) -> IncidentClimate:
        """Create incidents_climate."""
        db_obj = IncidentClimate(
            state=obj_in.state,
            year=obj_in.year,
            month=obj_in.month,
            n_incidents=obj_in.n_incidents,
            average_temperature=obj_in.average_temperature,
            average_precipitation=obj_in.average_precipitation,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # PUT
    def update(
        self, db: Session, *, db_obj: IncidentClimate, obj_in: IncidentClimateUpdate
    ) -> IncidentClimate:
        """Update incidents_climate."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    # DELETE
    def remove(self, db: Session, *, id: int) -> IncidentClimate:
        """Delete incidents_climate."""
        return super().remove(db, id=id)

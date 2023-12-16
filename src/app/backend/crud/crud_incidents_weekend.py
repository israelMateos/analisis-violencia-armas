"""CRUDIncidentsWeekend module."""
import sys

sys.path.append("src/app/backend")
from typing import Optional

from crud.base import CRUDBase  # pylint: disable=import-error
from models import IncidentWeekend  # pylint: disable=import-error
from schemas import (  # pylint: disable=import-error
    IncidentWeekendCreate,
    IncidentWeekendUpdate,
)
from sqlalchemy.orm import Session


class CRUDIncidentsWeekend(
    CRUDBase[IncidentWeekend, IncidentWeekendCreate, IncidentWeekendUpdate]
):
    # GET
    def get(self, db: Session, *, id: int) -> Optional[IncidentWeekend]:
        """Get incidents_weekend by id."""
        return super().get(db, id=id)

    def get_multi(self, db: Session) -> Optional[IncidentWeekend]:
        """Get all incidents_weekend."""
        return db.query(self.model).all()

    def get_multi_by_state(
        self, db: Session, *, state: str
    ) -> Optional[IncidentWeekend]:
        """Get all incidents_weekend by state."""
        return db.query(self.model).filter(self.model.state == state).all()

    def get_multi_by_year(self, db: Session, *, year: int) -> Optional[IncidentWeekend]:
        """Get all incidents_weekend by year."""
        return db.query(self.model).filter(self.model.year == year).all()

    def get_multi_by_state_and_year(
        self, db: Session, *, state: str, year: int
    ) -> Optional[IncidentWeekend]:
        """Get all incidents_weekend by state and year."""
        return (
            db.query(self.model)
            .filter(self.model.state == state, self.model.year == year)
            .all()
        )

    # POST
    def create(self, db: Session, *, obj_in: IncidentWeekendCreate) -> IncidentWeekend:
        """Create incidents_weekend."""
        db_obj = IncidentWeekend(
            state=obj_in.state,
            year=obj_in.year,
            is_weekend=obj_in.is_weekend,
            n_incidents_per_day=obj_in.n_incidents_per_day,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # PUT
    def update(
        self, db: Session, *, db_obj: IncidentWeekend, obj_in: IncidentWeekendUpdate
    ) -> IncidentWeekend:
        """Update incidents_weekend."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    # DELETE
    def remove(self, db: Session, *, id: int) -> IncidentWeekend:
        """Delete incidents_weekend."""
        return super().remove(db, id=id)

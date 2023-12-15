"""CRUDIncidentsWeekend module."""
import sys

sys.path.append("src/app")
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
    def get(self, db: Session, *, id: int) -> Optional[IncidentWeekend]:
        """Get incidents_weekend by id."""
        return db.query(self.model).filter(self.model.id == id).first()

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

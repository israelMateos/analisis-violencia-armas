"""CRUDIncidentsClimate module."""
import sys

sys.path.append("src/app")
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
    def get(self, db: Session, *, id: int) -> Optional[IncidentClimate]:
        """Get incidents_climate by id."""
        return db.query(self.model).filter(self.model.id == id).first()

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

"""CRUDIncidentsFirearmLaws module."""
import sys

sys.path.append("src/app")
from typing import Optional

from crud.base import CRUDBase  # pylint: disable=import-error
from models import IncidentFirearmLaws  # pylint: disable=import-error
from schemas import (  # pylint: disable=import-error
    IncidentFirearmLawsCreate,
    IncidentFirearmLawsUpdate,
)
from sqlalchemy.orm import Session


class CRUDIncidentsFirearmLaws(
    CRUDBase[IncidentFirearmLaws, IncidentFirearmLawsCreate, IncidentFirearmLawsUpdate]
):
    def get(self, db: Session, *, id: int) -> Optional[IncidentFirearmLaws]:
        """Get incidents_firearm_laws by id."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session) -> Optional[IncidentFirearmLaws]:
        """Get all incidents_firearm_laws."""
        return db.query(self.model).all()

    def get_multi_by_state(
        self, db: Session, *, state: str
    ) -> Optional[IncidentFirearmLaws]:
        """Get all incidents_firearm_laws by state."""
        return db.query(self.model).filter(self.model.state == state).all()

    def get_multi_by_year(
        self, db: Session, *, year: int
    ) -> Optional[IncidentFirearmLaws]:
        """Get all incidents_firearm_laws by year."""
        return db.query(self.model).filter(self.model.year == year).all()

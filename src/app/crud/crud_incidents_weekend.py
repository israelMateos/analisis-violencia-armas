"""CRUDIncidentsWeekend module."""
import sys

sys.path.append("src/app")
from typing import Optional

from sqlalchemy.orm import Session

from crud.base import CRUDBase  # pylint: disable=import-error
from models import IncidentWeekend  # pylint: disable=import-error
from schemas import IncidentWeekendCreate, IncidentWeekendUpdate  # pylint: disable=import-error


class CRUDIncidentsWeekend(CRUDBase[IncidentWeekend, IncidentWeekendCreate, IncidentWeekendUpdate]):
    def get_multi_by_state(self, db: Session, *, state: str) -> Optional[IncidentWeekend]:
        """Get all incidents_weekend by state."""
        return db.query(self.model).filter(self.model.state == state).all()

    def get_multi(self, db: Session) -> Optional[IncidentWeekend]:
        """Get all incidents_weekend."""
        return db.query(self.model).all()
    
    def get(self, db: Session, *, id: int) -> Optional[IncidentWeekend]:
        """Get incidents_weekend by id."""
        return db.query(self.model).filter(self.model.id == id).first()

"""CRUDIncidentsCombined module."""
import sys

sys.path.append("src/app")
from typing import Optional

from crud.base import CRUDBase  # pylint: disable=import-error
from models import IncidentCombined  # pylint: disable=import-error
from schemas import (  # pylint: disable=import-error
    IncidentCombinedCreate,
    IncidentCombinedUpdate,
)
from sqlalchemy.orm import Session


class CRUDIncidentsCombined(
    CRUDBase[IncidentCombined, IncidentCombinedCreate, IncidentCombinedUpdate]
):
    def get(self, db: Session, *, id: int) -> Optional[IncidentCombined]:
        """Get incidents_combined by id."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session) -> Optional[IncidentCombined]:
        """Get all incidents_combined."""
        return db.query(self.model).all()

    def get_multi_by_state(
        self, db: Session, *, state: str
    ) -> Optional[IncidentCombined]:
        """Get all incidents_combined by state."""
        return db.query(self.model).filter(self.model.state == state).all()

    def get_multi_by_year(
        self, db: Session, *, year: int
    ) -> Optional[IncidentCombined]:
        """Get all incidents_combined by year."""
        return db.query(self.model).filter(self.model.year == year).all()

"""CRUDIncidentsPopulationPoverty module."""
import sys

sys.path.append("src/app")
from typing import Optional

from crud.base import CRUDBase  # pylint: disable=import-error
from models import IncidentPopulationPoverty  # pylint: disable=import-error
from schemas import (  # pylint: disable=import-error
    IncidentPopulationPovertyCreate,
    IncidentPopulationPovertyUpdate,
)
from sqlalchemy.orm import Session


class CRUDIncidentsPopulationPoverty(
    CRUDBase[
        IncidentPopulationPoverty,
        IncidentPopulationPovertyCreate,
        IncidentPopulationPovertyUpdate,
    ]
):
    def get(self, db: Session, *, id: int) -> Optional[IncidentPopulationPoverty]:
        """Get incidents_population_poverty by id."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session) -> Optional[IncidentPopulationPoverty]:
        """Get all incidents_population_poverty."""
        return db.query(self.model).all()

    def get_multi_by_state(
        self, db: Session, *, state: str
    ) -> Optional[IncidentPopulationPoverty]:
        """Get all incidents_population_poverty by state."""
        return db.query(self.model).filter(self.model.state == state).all()

    def get_multi_by_year(
        self, db: Session, *, year: int
    ) -> Optional[IncidentPopulationPoverty]:
        """Get all incidents_population_poverty by year."""
        return db.query(self.model).filter(self.model.year == year).all()

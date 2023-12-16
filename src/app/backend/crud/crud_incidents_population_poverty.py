"""CRUDIncidentsPopulationPoverty module."""
import sys

sys.path.append("src/app/backend")
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
    # GET
    def get(self, db: Session, *, id: int) -> Optional[IncidentPopulationPoverty]:
        """Get incidents_population_poverty by id."""
        return super().get(db, id=id)

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

    def get_multi_by_state_and_year(
        self, db: Session, *, state: str, year: int
    ) -> Optional[IncidentPopulationPoverty]:
        """Get all incidents_population_poverty by state and year."""
        return (
            db.query(self.model)
            .filter(self.model.state == state, self.model.year == year)
            .all()
        )

    # POST
    def create(
        self, db: Session, *, obj_in: IncidentPopulationPovertyCreate
    ) -> IncidentPopulationPoverty:
        """Create incidents_population_poverty."""
        db_obj = IncidentPopulationPoverty(
            state=obj_in.state,
            year=obj_in.year,
            n_incidents=obj_in.n_incidents,
            poverty_rate=obj_in.poverty_rate,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # PUT
    def update(
        self,
        db: Session,
        *,
        db_obj: IncidentPopulationPoverty,
        obj_in: IncidentPopulationPovertyUpdate
    ) -> IncidentPopulationPoverty:
        """Update incidents_population_poverty."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    # DELETE
    def remove(self, db: Session, *, id: int) -> IncidentPopulationPoverty:
        """Remove incidents_population_poverty."""
        return super().remove(db, id=id)

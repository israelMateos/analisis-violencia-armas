"""CRUDIncidentsFirearmLaws module."""
import sys

sys.path.append("src/app/backend")
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
    # GET
    def get(self, db: Session, *, id: int) -> Optional[IncidentFirearmLaws]:
        """Get incidents_firearm_laws by id."""
        return super().get(db, id=id)

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

    def get_multi_by_state_and_year(
        self, db: Session, *, state: str, year: int
    ) -> Optional[IncidentFirearmLaws]:
        """Get all incidents_firearm_laws by state and year."""
        return (
            db.query(self.model)
            .filter(self.model.state == state, self.model.year == year)
            .all()
        )

    # POST
    def create(
        self, db: Session, *, obj_in: IncidentFirearmLawsCreate
    ) -> IncidentFirearmLaws:
        """Create incidents_firearm_laws."""
        db_obj = IncidentFirearmLaws(
            state=obj_in.state,
            year=obj_in.year,
            n_incidents=obj_in.n_incidents,
            lawtotal=obj_in.lawtotal,
            laws_1=obj_in.laws_1,
            laws_2=obj_in.laws_2,
            laws_3=obj_in.laws_3,
            laws_4=obj_in.laws_4,
            laws_5=obj_in.laws_5,
            laws_6=obj_in.laws_6,
            laws_7=obj_in.laws_7,
            laws_8=obj_in.laws_8,
            laws_9=obj_in.laws_9,
            laws_10=obj_in.laws_10,
            laws_11=obj_in.laws_11,
            laws_12=obj_in.laws_12,
            laws_13=obj_in.laws_13,
            laws_14=obj_in.laws_14,
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
        db_obj: IncidentFirearmLaws,
        obj_in: IncidentFirearmLawsUpdate
    ) -> IncidentFirearmLaws:
        """Update incidents_firearm_laws."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    # DELETE
    def remove(self, db: Session, *, id: int) -> IncidentFirearmLaws:
        """Remove incidents_firearm_laws."""
        return super().remove(db, id=id)

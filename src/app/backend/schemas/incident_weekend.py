import sys

sys.path.append("src/app/backend/")
from schemas.base import IncidentBase  # pylint: disable=import-error


class IncidentWeekend(IncidentBase):
    id: int
    is_weekend: int
    n_incidents_per_day: float


# Properties to receive on item creation
class IncidentWeekendCreate(IncidentBase):
    is_weekend: int
    n_incidents_per_day: float


# Properties to receive on item update
class IncidentWeekendUpdate(IncidentWeekendCreate):
    pass

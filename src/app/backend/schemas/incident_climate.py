import sys

sys.path.append("src/app/backend")
from schemas.base import IncidentBase  # pylint: disable=import-error


class IncidentClimate(IncidentBase):
    id: int
    month: int
    n_incidents: float
    average_temperature: float
    average_precipitation: float


# Properties to receive on item creation
class IncidentClimateCreate(IncidentBase):
    month: int
    n_incidents: float
    average_temperature: float
    average_precipitation: float


# Properties to receive on item update
class IncidentClimateUpdate(IncidentClimateCreate):
    pass

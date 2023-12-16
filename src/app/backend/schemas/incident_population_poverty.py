import sys

sys.path.append("src/app/backend")
from schemas.base import IncidentBase  # pylint: disable=import-error


class IncidentPopulationPoverty(IncidentBase):
    id: int
    poverty_rate: float
    n_incidents: float


# Properties to receive on item creation
class IncidentPopulationPovertyCreate(IncidentBase):
    poverty_rate: float
    n_incidents: float


# Properties to receive on item update
class IncidentPopulationPovertyUpdate(IncidentPopulationPovertyCreate):
    pass

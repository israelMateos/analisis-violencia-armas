# models.py
from pydantic import BaseModel


class IncidentBase(BaseModel):
    id: int
    state: str
    year: int


class IncidentPopulationPoverty(IncidentBase):
    poverty_rate: float
    n_incidents: float


# Properties to receive on item creation
class IncidentPopulationPovertyCreate(IncidentBase):
    poverty_rate: float
    n_incidents: float


# Properties to receive on item update
class IncidentPopulationPovertyUpdate(IncidentBase):
    poverty_rate: float
    n_incidents: float

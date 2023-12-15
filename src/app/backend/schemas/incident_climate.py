# models.py
from pydantic import BaseModel


class IncidentBase(BaseModel):
    id: int
    state: str
    year: int


class IncidentClimate(IncidentBase):
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
class IncidentClimateUpdate(IncidentBase):
    month: int
    n_incidents: float
    average_temperature: float
    average_precipitation: float

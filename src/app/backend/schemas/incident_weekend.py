# models.py
from pydantic import BaseModel


class IncidentBase(BaseModel):
    id: int
    state: str
    year: int


class IncidentWeekend(IncidentBase):
    is_weekend: int
    n_incidents_per_day: float


# Properties to receive on item creation
class IncidentWeekendCreate(IncidentBase):
    is_weekend: int
    n_incidents_per_day: float


# Properties to receive on item update
class IncidentWeekendUpdate(IncidentBase):
    is_weekend: int
    n_incidents_per_day: float

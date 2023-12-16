from pydantic import BaseModel


class IncidentBase(BaseModel):
    state: str
    year: int

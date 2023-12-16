import sys

sys.path.append("src/app/backend")
from schemas.base import IncidentBase  # pylint: disable=import-error

class IncidentCombined(IncidentBase):
    id: int
    n_incidents: float
    average_temperature: float
    average_precipitation: float
    poverty_rate: float
    lawtotal: int
    laws_1: int
    laws_2: int
    laws_3: int
    laws_4: int
    laws_5: int
    laws_6: int
    laws_7: int
    laws_8: int
    laws_9: int
    laws_10: int
    laws_11: int
    laws_12: int
    laws_13: int
    laws_14: int


# Properties to receive on item creation
class IncidentCombinedCreate(IncidentBase):
    n_incidents: float
    average_temperature: float
    average_precipitation: float
    poverty_rate: float
    lawtotal: int
    laws_1: int
    laws_2: int
    laws_3: int
    laws_4: int
    laws_5: int
    laws_6: int
    laws_7: int
    laws_8: int
    laws_9: int
    laws_10: int
    laws_11: int
    laws_12: int
    laws_13: int
    laws_14: int


# Properties to receive on item update
class IncidentCombinedUpdate(IncidentCombined):
    pass

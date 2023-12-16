import sys

sys.path.append("src/app/backend")
from sqlalchemy import BigInteger, Column, Double, Integer, String, Table

from db import Base  # pylint: disable=import-error


class IncidentWeekend(Base):
    __table__ = Table(
        "incidents_weekend",
        Base.metadata,
        Column("id", Integer, primary_key=True, nullable=False, autoincrement=True),
        Column("state", String),
        Column("year", BigInteger),
        Column("is_weekend", BigInteger),
        Column("n_incidents_per_day", BigInteger),
        schema="gold",
    )


class IncidentClimate(Base):
    __table__ = Table(
        "incidents_climate",
        Base.metadata,
        Column("id", Integer, primary_key=True, nullable=False, autoincrement=True),
        Column("state", String),
        Column("year", BigInteger),
        Column("month", BigInteger),
        Column("n_incidents", BigInteger),
        Column("average_temperature", Double),
        Column("average_precipitation", Double),
        schema="gold",
    )


class IncidentPopulationPoverty(Base):
    __table__ = Table(
        "incidents_population_poverty",
        Base.metadata,
        Column("id", Integer, primary_key=True, nullable=False, autoincrement=True),
        Column("state", String),
        Column("year", BigInteger),
        Column("poverty_rate", Double),
        Column("n_incidents", BigInteger),
        schema="gold",
    )


class IncidentFirearmLaws(Base):
    __table__ = Table(
        "incidents_firearm_laws",
        Base.metadata,
        Column("id", Integer, primary_key=True, nullable=False, autoincrement=True),
        Column("state", String),
        Column("year", BigInteger),
        Column("n_incidents", BigInteger),
        Column("lawtotal", BigInteger),
        Column("laws_1", BigInteger),
        Column("laws_2", BigInteger),
        Column("laws_3", BigInteger),
        Column("laws_4", BigInteger),
        Column("laws_5", BigInteger),
        Column("laws_6", BigInteger),
        Column("laws_7", BigInteger),
        Column("laws_8", BigInteger),
        Column("laws_9", BigInteger),
        Column("laws_10", BigInteger),
        Column("laws_11", BigInteger),
        Column("laws_12", BigInteger),
        Column("laws_13", BigInteger),
        Column("laws_14", BigInteger),
        schema="gold",
    )


class IncidentCombined(Base):
    __table__ = Table(
        "incidents_combined",
        Base.metadata,
        Column("id", Integer, primary_key=True, nullable=False, autoincrement=True),
        Column("state", String),
        Column("year", BigInteger),
        Column("n_incidents", BigInteger),
        Column("average_temperature", Double),
        Column("average_precipitation", Double),
        Column("poverty_rate", Double),
        Column("lawtotal", BigInteger),
        Column("laws_1", BigInteger),
        Column("laws_2", BigInteger),
        Column("laws_3", BigInteger),
        Column("laws_4", BigInteger),
        Column("laws_5", BigInteger),
        Column("laws_6", BigInteger),
        Column("laws_7", BigInteger),
        Column("laws_8", BigInteger),
        Column("laws_9", BigInteger),
        Column("laws_10", BigInteger),
        Column("laws_11", BigInteger),
        Column("laws_12", BigInteger),
        Column("laws_13", BigInteger),
        Column("laws_14", BigInteger),
        schema="gold",
    )

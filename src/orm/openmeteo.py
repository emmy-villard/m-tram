from sqlalchemy import TIMESTAMP, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from orm.base import Base
from datetime import datetime

class OpenMeto(Base):
    """
    Class definition of table : "openmeteo". Used to store Open-meteo data for Grenoble

    Properties
    ----------
    time : sqlalchemy.mapped_column(sqlalchemy.TIMESTAMP)
        timestamp
    temperature_2m : sqlalchemy.mapped_column(sqlalchemy.Float)
        temperature 2m above the ground
    apparent_temperature : sqlalchemy.mapped_column(sqlalchemy.Float)
        apparent temperature (feel)
    relativehumidity_2m : sqlalchemy.mapped_column(sqlalchemy.Integer)
        relative humidity 2m above the ground
    precipitation : sqlalchemy.mapped_column(sqlalchemy.Float)
        rain + snow precipitations
    rain : sqlalchemy.mapped_column(sqlalchemy.Float)
        Rain precipitations
    snow : sqlalchemy.mapped_column(sqlalchemy.Float)
        Snow precipitations
    weathercode : sqlalchemy.mapped_column(sqlalchemy.Integer)
        Weather condition as a numeric code (WMO weather interpretation codes)
    pressure_msl : sqlalchemy.mapped_column(sqlalchemy.Float)
        atmo pressure at sea level
    cloudcover :sqlalchemy.mapped_column(sqlalchemy.Integer)
        clouv cover percentage (0 to 100)
    windspeed_10m : sqlalchemy.mapped_column(sqlalchemy.Float)
        Wind speed 10m above the ground
    windgusts_10m : sqlalchemy.mapped_column(sqlalchemy.Float)
        Wind gust 10m above the ground
    
    """
    __tablename__ = "openmeteo"

    time: Mapped[datetime] = mapped_column(TIMESTAMP, primary_key=True)
    temperature_2m: Mapped[float] = mapped_column(Float)
    apparent_temperature: Mapped[float] = mapped_column(Float)
    relativehumidity_2m: Mapped[int] = mapped_column(Integer)
    precipitation: Mapped[float] = mapped_column(Float)
    rain: Mapped[float] = mapped_column(Float)
    snowfall: Mapped[float] = mapped_column(Float)
    weathercode: Mapped[int] = mapped_column(Integer)
    pressure_msl: Mapped[float] = mapped_column(Float)
    cloudcover: Mapped[int] = mapped_column(Integer)
    windspeed_10m: Mapped[float] = mapped_column(Float)
    windgusts_10m: Mapped[float] = mapped_column(Float)


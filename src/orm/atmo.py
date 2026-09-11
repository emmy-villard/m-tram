from sqlalchemy import TIMESTAMP, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from orm.base import Base
from datetime import datetime

class Atmo(Base):
    """
    Class definition of table : "openmeteo". Used to store Open-meteo data for Grenoble

    Properties
    ----------
    time : sqlalchemy.mapped_column(sqlalchemy.TIMESTAMP)
        timestamp
    pollution_index : sqlalchemy.mapped_column(sqlalchemy.Integer)
        Pollution index (max of sub-indexes)
    is_value_mesured : sqlalchemy.mapped_column(sqlalchemy.Boolean)
        whether value is mesured (True) or estimated (False)
    PM10_index : sqlalchemy.mapped_column(sqlalchemy.Integer)
        PM10 pollution index
    PM2_5_index : sqlalchemy.mapped_column(sqlalchemy.Integer)
        PM2.5 pollution index
    O3_index : sqlalchemy.mapped_column(sqlalchemy.Integer)
        O3 pollution index
    NO2_index : sqlalchemy.mapped_column(sqlalchemy.Integer)
        NO2 pollution index
    SO2_index : sqlalchemy.mapped_column(sqlalchemy.Integer)
        SO2 pollution index
    """
    __tablename__ = "atmo"

    time: Mapped[datetime] = mapped_column(TIMESTAMP, primary_key=True)
    pollution_index: Mapped[int] = mapped_column(Integer)
    is_value_mesured: Mapped[bool] = mapped_column(Boolean)
    PM10_index: Mapped[int] = mapped_column(Integer)
    PM2_5_index: Mapped[int] = mapped_column(Integer)
    O3_index: Mapped[int] = mapped_column(Integer)
    NO2_index: Mapped[int] = mapped_column(Integer)
    SO2_index: Mapped[int] = mapped_column(Integer)


from sqlalchemy import TIMESTAMP, Float, Text
from sqlalchemy.orm import Mapped, mapped_column
from orm.base import Base
from datetime import datetime

class HourlyAggregate(Base):
    """
    Class definition of table: "dashboard_hourly_aggregates".
    Stores hourly traffic and environmental aggregates for the dashboard.

    Properties
    ----------
    hour_start : sqlalchemy.mapped_column(sqlalchemy.TIMESTAMP)
        Start of the aggregated hour
    traffic_type : sqlalchemy.mapped_column(sqlalchemy.Text)
        Traffic source, either tram or road
    """
    __tablename__ = "dashboard_hourly_aggregates"

    hour_start: Mapped[datetime] = mapped_column(TIMESTAMP, primary_key=True)
    traffic_type: Mapped[str] = mapped_column(Text, primary_key=True)
    average_congestion_level: Mapped[float] = mapped_column(Float)
    pollution_index: Mapped[float] = mapped_column(Float)
    pm10_index: Mapped[float] = mapped_column(Float)
    pm2_5_index: Mapped[float] = mapped_column(Float)
    o3_index: Mapped[float] = mapped_column(Float)
    no2_index: Mapped[float] = mapped_column(Float)
    so2_index: Mapped[float] = mapped_column(Float)
    precipitation_total: Mapped[float] = mapped_column(Float)
    rainfall_total: Mapped[float] = mapped_column(Float)
    average_temperature: Mapped[float] = mapped_column(Float)
    average_relative_humidity: Mapped[float] = mapped_column(Float)
    average_cloud_cover: Mapped[float] = mapped_column(Float)
    average_wind_speed: Mapped[float] = mapped_column(Float)


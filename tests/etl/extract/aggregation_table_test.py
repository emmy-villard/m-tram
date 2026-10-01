from datetime import datetime
from sqlalchemy.orm import Session
from orm.base import Base
from orm.ligne import Ligne
from orm.trr import Trr
from orm.openmeteo import OpenMeto
from orm.atmo import Atmo
from db_connection.test_engine import engine
import pytest

from etl.extract.aggregation_table import get_select_stmt, get_columns

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
    engine.dispose()

def test_get_select_stmt_aggregates_hour():
    hour = datetime(2026, 1, 1, 10, 0, 0)
    with Session(engine) as session:
        session.add(Ligne(
            ligne_id="1", ligne_time=hour, ligne_nsv_id=2
        ))
        session.add(Ligne(
            ligne_id="2", ligne_time=hour.replace(minute=30), ligne_nsv_id=4
        ))
        session.add(Trr(
            trr_id="1", trr_time=hour, trr_nsv_id=1
        ))
        session.add(Atmo(
            time=hour, pollution_index=10, is_value_mesured=True,
            PM10_index=1, PM2_5_index=2, O3_index=3, NO2_index=4,
            SO2_index=5
        ))
        session.add(OpenMeto(
            time=hour, temperature_2m=10.0, apparent_temperature=9.0,
            relativehumidity_2m=50, precipitation=1.0, rain=1.0,
            snowfall=0.0, weathercode=0, pressure_msl=1000.0,
            cloudcover=20, windspeed_10m=5.0, windgusts_10m=8.0
        ))
        session.commit()

        stmt = get_select_stmt(hour)
        result = session.execute(stmt).mappings().one()

    assert result["hour"] == hour
    assert result["mean_tram_traffic"] == 3
    assert result["mean_road_traffic"] == 1
    assert result["mean_pollution_index"] == 10
    assert result["mean_temperature"] == 10.0
    assert result["precipitation_1h"] == 1.0
    assert result["rain_1h"] == 1.0

def test_get_columns_matches_select_stmt_fields():
    hour = datetime(2026, 1, 1, 10, 0, 0)
    with Session(engine) as session:
        session.add(OpenMeto(
            time=hour, temperature_2m=10.0, apparent_temperature=9.0,
            relativehumidity_2m=50, precipitation=1.0, rain=1.0,
            snowfall=0.0, weathercode=0, pressure_msl=1000.0,
            cloudcover=20, windspeed_10m=5.0, windgusts_10m=8.0
        ))
        session.add(Atmo(
            time=hour, pollution_index=10, is_value_mesured=True,
            PM10_index=1, PM2_5_index=2, O3_index=3, NO2_index=4,
            SO2_index=5
        ))
        session.commit()

        stmt = get_select_stmt(hour)
        result = session.execute(stmt).mappings().one()

    assert len(get_columns()) == len(result.keys())

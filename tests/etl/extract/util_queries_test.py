from datetime import datetime
from sqlalchemy.orm import Session
from orm.base import Base
from orm.ligne import Ligne
from orm.trr import Trr
from orm.openmeteo import OpenMeto
from orm.atmo import Atmo
from db_connection.test_engine import engine
import pytest

from etl.extract.util_queries import get_earliest_date_in_db

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
    engine.dispose()

def test_get_earliest_date_in_db():
    with Session(engine) as session:
        session.add_all([
            Ligne(
                ligne_id="1", ligne_time=datetime(2026, 1, 3), ligne_nsv_id=1
            ),
            Ligne (
                ligne_id="1", ligne_time=datetime(2026, 2, 3), ligne_nsv_id=1
            )
        ])

        session.add(Trr(
            trr_id="1", trr_time=datetime(2026, 1, 2), trr_nsv_id=1
        ))
        session.add(OpenMeto(
            time=datetime(2026, 1, 1), temperature_2m=1.0,
            apparent_temperature=1.0, relativehumidity_2m=1,
            precipitation=0.0, rain=0.0, snowfall=0.0, weathercode=0,
            pressure_msl=1.0, cloudcover=0, windspeed_10m=1.0,
            windgusts_10m=1.0
        ))
        session.add(Atmo(
            time=datetime(2026, 1, 4), pollution_index=1,
            is_value_mesured=True, PM10_index=1, PM2_5_index=1,
            O3_index=1, NO2_index=1, SO2_index=1
        ))
        session.commit()

    assert get_earliest_date_in_db([Ligne, Trr, OpenMeto, Atmo]) == \
        datetime(2026, 1, 1)

def test_get_earliest_date_in_db_one_empty():
    with Session(engine) as session:
        session.add(Ligne(
            ligne_id="1", ligne_time=datetime(2026, 1, 3), ligne_nsv_id=1
        ))
        session.add(Trr(
            trr_id="1", trr_time=datetime(2026, 1, 2), trr_nsv_id=1
        ))
        session.add(Atmo(
            time=datetime(2026, 1, 4), pollution_index=1,
            is_value_mesured=True, PM10_index=1, PM2_5_index=1,
            O3_index=1, NO2_index=1, SO2_index=1
        ))
        session.commit()

    assert get_earliest_date_in_db([Ligne, Trr, OpenMeto, Atmo]) == \
        datetime(2026, 1, 2)

def test_get_earliest_date_in_db_ignores_empty_tables():
    with Session(engine) as session:
        session.add(Ligne(
            ligne_id="1", ligne_time=datetime(2026, 1, 5), ligne_nsv_id=1
        ))
        session.commit()

    assert get_earliest_date_in_db([Ligne, Trr, OpenMeto, Atmo]) == \
        datetime(2026, 1, 5)

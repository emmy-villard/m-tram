from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from orm.base import Base
from orm.ligne import Ligne
from orm.trr import Trr
from orm.openmeteo import OpenMeto
from orm.atmo import Atmo
from orm.hourlyagg import HourlyAggregate
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
        results = session.execute(stmt).mappings().all()

    # One row per (hour, traffic_type): "road" sorts before "tram".
    assert len(results) == 2
    road_result, tram_result = results

    assert road_result["hour_start"] == hour
    assert road_result["traffic_type"] == "road"
    assert road_result["average_congestion_level"] == 1

    assert tram_result["hour_start"] == hour
    assert tram_result["traffic_type"] == "tram"
    assert tram_result["average_congestion_level"] == 3

    for result in results:
        assert result["pollution_index"] == 10
        assert result["average_temperature"] == 10.0
        assert result["precipitation_total"] == 1.0
        assert result["rainfall_total"] == 1.0

def test_get_columns_matches_select_stmt_fields():
    hour = datetime(2026, 1, 1, 10, 0, 0)
    with Session(engine) as session:
        session.add(Ligne(
            ligne_id="1", ligne_time=hour, ligne_nsv_id=2
        ))
        session.add(Trr(
            trr_id="1", trr_time=hour, trr_nsv_id=1
        ))
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
        result = session.execute(stmt).mappings().first()

    assert result is not None
    assert len(get_columns()) == len(result.keys())
    assert set(get_columns()) == set(result.keys())


def test_get_select_stmt_uses_atmo_index_for_matching_day(monkeypatch):
    first_hour = datetime(2026, 1, 1, 10, 0, 0)
    second_hour = datetime(2026, 1, 2, 10, 0, 0)
    monkeypatch.setattr(
        "etl.extract.aggregation_table.get_earliest_date_in_db",
        lambda: first_hour.replace(hour=0)
    )

    with Session(engine) as session:
        session.add_all([
            Ligne(ligne_id="1", ligne_time=first_hour, ligne_nsv_id=2),
            Ligne(ligne_id="2", ligne_time=second_hour, ligne_nsv_id=4),
            Trr(trr_id="1", trr_time=first_hour, trr_nsv_id=1),
            Trr(trr_id="2", trr_time=second_hour, trr_nsv_id=3),
            Atmo(
                time=first_hour, pollution_index=2, is_value_mesured=True,
                PM10_index=1, PM2_5_index=2, O3_index=3, NO2_index=4,
                SO2_index=5
            ),
            Atmo(
                time=second_hour, pollution_index=5, is_value_mesured=True,
                PM10_index=2, PM2_5_index=3, O3_index=4, NO2_index=5,
                SO2_index=6
            ),
            OpenMeto(
                time=first_hour, temperature_2m=10.0, apparent_temperature=9.0,
                relativehumidity_2m=50, precipitation=1.0, rain=1.0,
                snowfall=0.0, weathercode=0, pressure_msl=1000.0,
                cloudcover=20, windspeed_10m=5.0, windgusts_10m=8.0
            ),
            OpenMeto(
                time=second_hour, temperature_2m=10.0, apparent_temperature=9.0,
                relativehumidity_2m=50, precipitation=1.0, rain=1.0,
                snowfall=0.0, weathercode=0, pressure_msl=1000.0,
                cloudcover=20, windspeed_10m=5.0, windgusts_10m=8.0
            ),
        ])
        session.commit()

        results = session.execute(get_select_stmt(None)).mappings().all()

    pollution_by_hour = {
        (result["hour_start"], result["traffic_type"]): result["pollution_index"]
        for result in results
    }
    assert pollution_by_hour == {
        (first_hour, "tram"): 2,
        (first_hour, "road"): 2,
        (second_hour, "tram"): 5,
        (second_hour, "road"): 5,
    }


def test_get_select_stmt_only_emits_row_for_traffic_source_with_data():
    """
    An hour with only tram data (no road data) should only produce a
    "tram" row, and vice versa: "average_congestion_level" is NOT NULL
    on HourlyAggregate, so rows can't be emitted for a traffic source
    that has no data for that hour.
    """
    tram_only_hour = datetime(2026, 1, 1, 10, 0, 0)
    road_only_hour = datetime(2026, 1, 1, 11, 0, 0)
    no_traffic_hour = datetime(2026, 1, 1, 12, 0, 0)

    with Session(engine) as session:
        for hour in (tram_only_hour, road_only_hour, no_traffic_hour):
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
        session.add(Ligne(
            ligne_id="1", ligne_time=tram_only_hour, ligne_nsv_id=2
        ))
        session.add(Trr(
            trr_id="1", trr_time=road_only_hour, trr_nsv_id=1
        ))
        session.commit()

        stmt = get_select_stmt(tram_only_hour)
        results = session.execute(stmt).mappings().all()

    rows_by_hour = {}
    for result in results:
        rows_by_hour.setdefault(result["hour_start"], []).append(
            result["traffic_type"]
        )

    assert rows_by_hour[tram_only_hour] == ["tram"]
    assert rows_by_hour[road_only_hour] == ["road"]
    assert no_traffic_hour not in rows_by_hour

def test_insert_from_select_does_not_violate_not_null_constraint():
    """
    Regression test: inserting the select statement straight into
    HourlyAggregate (as the increment/remake DAGs do) must not raise
    an IntegrityError even when some hours only have tram or road data.
    """
    tram_only_hour = datetime(2026, 1, 1, 10, 0, 0)
    road_only_hour = datetime(2026, 1, 1, 11, 0, 0)
    no_traffic_hour = datetime(2026, 1, 1, 12, 0, 0)

    with Session(engine) as session:
        for hour in (tram_only_hour, road_only_hour, no_traffic_hour):
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
        session.add(Ligne(
            ligne_id="1", ligne_time=tram_only_hour, ligne_nsv_id=2
        ))
        session.add(Trr(
            trr_id="1", trr_time=road_only_hour, trr_nsv_id=1
        ))
        session.commit()

        stmt = get_select_stmt(tram_only_hour)
        insert_stmt = insert(HourlyAggregate).from_select(
            get_columns(), stmt
        )
        session.execute(insert_stmt)
        session.commit()

        rows = {
            (row.hour_start, row.traffic_type): row.average_congestion_level
            for row in session.query(HourlyAggregate).all()
        }

    assert rows == {
        (tram_only_hour, "tram"): 2.0,
        (road_only_hour, "road"): 1.0,
    }

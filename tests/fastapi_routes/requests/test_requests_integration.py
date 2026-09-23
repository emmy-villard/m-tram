from etl.classes.Ligne import Ligne
from etl.classes.Trr import Trr
from etl.classes.OpenMeteo import OpenMeteo
from etl.classes.Atmo import Atmo

from fastapi_routes.requests import raw, count
from orm.base import Base
from db_connection.test_engine import engine
import pytest
import pandas as pd
import os
import io
import asyncio
import tempfile

TEST_DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "..", "etl", "etl_test_data"
)

def _load_csv(filename):
    dataframe = pd.read_csv(os.path.join(TEST_DATA_DIR, filename))
    return dataframe

"""
Setup the database
"""
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Ligne.load_table(_load_csv("ligne.csv"), engine,
        Ligne.orm_class(), Ligne.data_validator())
    Trr.load_table(_load_csv("trr.csv"), engine,
        Trr.orm_class(), Trr.data_validator())
    OpenMeteo.load_table(_load_csv("openmeteo.csv"), engine,
        OpenMeteo.orm_class(), OpenMeteo.data_validator())
    Atmo.load_table(_load_csv("atmo.csv"), engine,
        Atmo.orm_class(), Atmo.data_validator())

    yield
    Base.metadata.drop_all(engine)
    engine.dispose()

def test_get_raw_data_ligne():
    expected = _load_csv("ligne.csv")
    rows = raw.get_data("ligne")
    assert len(rows) == len(expected)
    result_df = pd.DataFrame(
        [(row.ligne_id, row.ligne_nsv_id) for row in rows],
        columns=["ligne_id", "ligne_nsv_id"]
    ).sort_values("ligne_id").reset_index(drop=True)
    expected_df = expected[["ligne_id", "ligne_nsv_id"]] \
        .sort_values("ligne_id").reset_index(drop=True)
    assert result_df.equals(expected_df)

def test_get_raw_data_trr():
    expected = _load_csv("trr.csv")
    rows = raw.get_data("trr")
    assert len(rows) == len(expected)
    result_df = pd.DataFrame(
        [(row.trr_id, row.trr_nsv_id) for row in rows],
        columns=["trr_id", "trr_nsv_id"]
    ).sort_values("trr_id").reset_index(drop=True)
    expected_df = expected[["trr_id", "trr_nsv_id"]] \
        .sort_values("trr_id").reset_index(drop=True)
    assert result_df.equals(expected_df)

def test_get_raw_data_openmeteo():
    expected = _load_csv("openmeteo.csv")
    rows = raw.get_data("openmeteo")
    assert len(rows) == len(expected)
    result_df = pd.DataFrame(
        [(pd.Timestamp(row.time), row.temperature_2m) for row in rows],
        columns=["time", "temperature_2m"]
    ).sort_values("time").reset_index(drop=True)
    expected_df = expected[["time", "temperature_2m"]].assign(
        time=lambda df: pd.to_datetime(df["time"])
    ).sort_values("time").reset_index(drop=True)
    assert result_df.equals(expected_df)

def test_get_raw_data_atmo():
    expected = _load_csv("atmo.csv")
    rows = raw.get_data("atmo")
    assert len(rows) == len(expected)
    result_df = pd.DataFrame(
        [(pd.Timestamp(row.time), row.pollution_index) for row in rows],
        columns=["time", "pollution_index"]
    ).sort_values("time").reset_index(drop=True)
    expected_df = expected[["time", "pollution_index"]].assign(
        time=lambda df: pd.to_datetime(df["time"])
    ).sort_values("time").reset_index(drop=True)
    assert result_df.equals(expected_df)

async def _read_csv_response(response):
    chunks = []
    async for chunk in response.body_iterator:
        if isinstance(chunk, str):
            chunks.append(chunk.encode("utf-8"))
        else:
            chunks.append(chunk)
    return b"".join(chunks).decode("utf-8")

def test_stream_csv_ligne():
    expected = _load_csv("ligne.csv")
    response = raw.stream_csv(raw._get_model("ligne"))
    assert response.media_type == "text/csv"
    payload = asyncio.run(_read_csv_response(response))
    rows = pd.read_csv(io.StringIO(payload))
    result_df = rows[["ligne_id", "ligne_nsv_id"]].sort_values("ligne_id").reset_index(drop=True)
    expected_df = expected[["ligne_id", "ligne_nsv_id"]].sort_values("ligne_id").reset_index(drop=True)
    assert len(rows) == len(expected)
    assert result_df.equals(expected_df)

def test_round_trip_csv_to_database_ligne():
    original = _load_csv("ligne.csv")
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as tmp:
        original.to_csv(tmp.name, index=False)
        tmp_path = tmp.name

    try:
        reloaded = pd.read_csv(tmp_path)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        Ligne.load_table(reloaded, engine, Ligne.orm_class(), Ligne.data_validator())

        actual_df = pd.read_sql_query(
            "SELECT ligne_id, ligne_time, ligne_nsv_id FROM ligne ORDER BY ligne_id, ligne_time",
            engine,
        )
        actual_df["ligne_time"] = pd.to_datetime(actual_df["ligne_time"])

        expected_df = original[["ligne_id", "ligne_time", "ligne_nsv_id"]].copy()
        expected_df["ligne_time"] = pd.to_datetime(expected_df["ligne_time"])
        expected_df = expected_df.sort_values(["ligne_id", "ligne_time"]).reset_index(drop=True)
        actual_df = actual_df.sort_values(["ligne_id", "ligne_time"]).reset_index(drop=True)

        assert actual_df.equals(expected_df)
    finally:
        os.unlink(tmp_path)


def test_get_count():
    result = count.get_data()
    ligne_len = len(_load_csv("ligne.csv"))
    assert ligne_len != 0
    assert result["ligne"] == ligne_len



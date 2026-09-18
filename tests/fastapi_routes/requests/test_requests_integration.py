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

def test_get_count():
    result = count.get_data()
    ligne_len = len(_load_csv("ligne.csv"))
    trr_len = len(_load_csv("trr.csv"))
    openmeteo_len = len(_load_csv("openmeteo.csv"))
    atmo_len = len(_load_csv("atmo.csv"))
    assert ligne_len != 0
    assert trr_len != 0
    assert openmeteo_len != 0
    assert atmo_len != 0
    assert result["ligne"] == ligne_len
    assert result["trr"] == trr_len
    assert result["openmeteo"] == openmeteo_len
    assert result["atmo"] == atmo_len
    assert result["total"] == ligne_len + trr_len + openmeteo_len + atmo_len



from etl.transform.meteo import raw_to_pandas_meteo, process_meteo_data
import numpy as np
import os, json
from datetime import datetime
import pytest

@pytest.fixture
def raw_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/../etl_test_data/openmeteo.json") as file:
        return json.load(file)

@pytest.mark.parametrize(["key", "value", "end_value"], [
    [
        "time", "2026-02-04T03:23",
        datetime(year=2026, month=2, day=4, hour=3, minute=23)
    ],
    ["temperature_2m", 43.3, 43.3],
    ["random_key_342", 34.0, 34]
])
def test_process_meteo_data_correct(key, value, end_value):
    assert process_meteo_data(key, value) == end_value

@pytest.mark.parametrize(["key", "value", "end_value"], [
    [
        "time", "2026-02-04T03:00",
        datetime(year=2026, month=2, day=4, hour=3, minute=23)
    ],
    ["temperature_2m", 43.3, 8],
])
def test_process_meteo_data_incorrect(key, value, end_value):
    assert process_meteo_data(key, value) != end_value

def test_empty_dataframe():
    with pytest.raises(ValueError):
        raw_to_pandas_meteo({})

def test_full_dataframe(raw_data):
    dataframe = raw_to_pandas_meteo(raw_data).reset_index()
    for k, v in raw_data["hourly"].items():
        values = np.asarray([process_meteo_data(k, val) for val in v])
        assert np.all(np.equal(dataframe[k].values, values))

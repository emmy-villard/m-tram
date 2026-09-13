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
        "time",
        "2026-02-04T03:23",
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

def test_missing_data_no_errors():
    raw_data = {
        "hourly": {
            "time": ["2026-01-01T00:00", "2026-01-01T01:00"],
            "temperature_2m": [0.0],
            "apparent_temperature": [0.0, 1.0],
            "relativehumidity_2m": [45, 47],
            "precipitation": [0.0, 0.0],
            "rain": [0.0, 0.0],
            "snowfall": [0.0, 0.0],
            "weathercode": [1, 2],
            "pressure_msl": [1012.0, 1011.0],
            "cloudcover": [10, 20],
            "windspeed_10m": [3.5, 5.5],
            "windgusts_10m": [7.8, 8.9],
        }
    }
    valid_raw_data = {
        "hourly": {
            "time": ["2026-01-01T00:00"],
            "temperature_2m": [0.0],
            "apparent_temperature": [0.0],
            "relativehumidity_2m": [45],
            "precipitation": [0.0],
            "rain": [0.0],
            "snowfall": [0.0],
            "weathercode": [1],
            "pressure_msl": [1012.0],
            "cloudcover": [10],
            "windspeed_10m": [3.5],
            "windgusts_10m": [7.8],
        }
    }
    dataframe_result = raw_to_pandas_meteo(raw_data)
    assert not dataframe_result.empty
    assert dataframe_result.equals(raw_to_pandas_meteo(valid_raw_data))

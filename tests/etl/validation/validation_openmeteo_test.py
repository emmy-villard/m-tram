from etl.validation_schemas.openmeteo import convert_openmeteo_data
from datetime import datetime, timedelta
import os
import pandas as pd
import pytest

def to_openmeteo_df(data):
    columns = [
        "time",
        "temperature_2m",
        "apparent_temperature",
        "relativehumidity_2m",
        "precipitation",
        "rain",
        "snowfall",
        "weathercode",
        "pressure_msl",
        "cloudcover",
        "windspeed_10m",
        "windgusts_10m"
    ]
    dataframe = pd.DataFrame(data, columns=columns).set_index("time")
    return dataframe

def test_validate_static_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dataframe = pd.read_csv(dir_path + "/../etl_test_data/openmeteo.csv")
    convert_openmeteo_data(dataframe)

def test_value_error_duplicated_primary_key():
    datetime_value = datetime.now()
    dataframe = to_openmeteo_df([
        [datetime_value, 20.0, 21.0, 70, 0.0, 0.0, 0.0, 1, 1012.0, 20, 1.5, 2.7],
        [datetime_value, 21.0, 22.0, 72, 0.0, 0.0, 0.0, 1, 1012.0, 25, 2.0, 3.0],
        [datetime_value, 22.0, 23.0, 75, 0.0, 0.0, 0.0, 2, 1012.5, 30, 2.8, 4.0],
    ])
    with pytest.raises(ValueError):
        convert_openmeteo_data(dataframe)

def test_no_errors():
    datetime_value = datetime.now()
    dataframe = to_openmeteo_df([
        [datetime_value, 20.0, 21.0, 70, 0.0, 0.0, 0.0, 1, 1012.0, 20, 1.5, 2.7],
        [datetime_value + timedelta(hours=1), 19.5, 20.2, 72, 0.0, 0.0, 0.0, 1, 1013.0, 25, 2.0, 3.0],
    ])
    convert_openmeteo_data(dataframe)

def test_errors():
    datetime_value = datetime.now()
    dataframe = to_openmeteo_df([
        [datetime_value, 20.0, 21.0, 70, 0.0, 0.0, 0.0, 1, 1012.0, 20, 1.5, 2.7],
        [datetime_value + timedelta(seconds=2), 21.0, 22.0, 72, 0.0, 0.0, 0.0, 1, 1012.0, 25, 2.0, 3.0],
    ])
    convert_openmeteo_data(dataframe)

def test_value_error_empty():
    with pytest.raises(ValueError):
        convert_openmeteo_data(pd.DataFrame())
from etl.validation_schemas.atmo import validate_atmo_data
from datetime import datetime, timedelta
import os
import pandas as pd
import pytest

def to_atmo_df(data):
    columns = [
        "time",
        "pollution_index",
        "is_value_mesured",
        "PM10_index",
        "PM2_5_index",
        "O3_index",
        "NO2_index",
        "SO2_index",
    ]
    dataframe = pd.DataFrame(data, columns=columns)
    return dataframe

def test_validate_static_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dataframe = pd.read_csv(dir_path + "/../etl_test_data/atmo.csv")
    validate_atmo_data(dataframe)

def test_value_error_duplicated_primary_key():
    datetime_value = datetime.now()
    dataframe = to_atmo_df([
        [datetime_value, 1, True, 2, 1, 2, 3, 5],
        [datetime_value, 1, True, 2, 1, 2, 3, 5],
    ])
    with pytest.raises(ValueError):
        validate_atmo_data(dataframe)

def test_value_error_pollution_index_out_of_bounds():
    datetime_value = datetime.now()
    dataframe = to_atmo_df([
        [datetime_value, 0, True, 2, 1, 2, 3, 5],
        [datetime_value + timedelta(seconds=-2), 1, True, 2, 1, 2, 3, 5],
    ])
    with pytest.raises(ValueError):
        validate_atmo_data(dataframe)

def test_no_errors():
    datetime_value = datetime.now()
    dataframe = to_atmo_df([
        [datetime_value, 6, True, 2, 1, 2, 3, 5],
        [datetime_value + timedelta(seconds=-2), 1, True, 2, 1, 2, 3, 5],
    ])
    validate_atmo_data(dataframe)

def test_value_error_empty():
    with pytest.raises(ValueError):
        validate_atmo_data(pd.DataFrame())
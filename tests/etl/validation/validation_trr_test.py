from etl.validation_schemas.trr import convert_trr_data
from datetime import datetime, timedelta
import os
import pandas as pd
import pytest

def to_trr_df(data):
    columns = ["trr_id", "trr_time", "trr_nsv_id"]
    dataframe = pd.DataFrame(data, columns=columns).set_index("trr_id")
    return dataframe

def test_validate_static_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dataframe = pd.read_csv(dir_path + "/../etl_test_data/trr.csv")
    convert_trr_data(dataframe)

def test_value_error_duplicated_primary_key():
    datetime_value = datetime.now()
    dataframe = to_trr_df([
        ["id1", datetime_value, 3],
        ["id2", datetime_value, 1],
        ["id1", datetime_value, 1]
    ])
    with pytest.raises(ValueError):
        convert_trr_data(dataframe)

def test_no_errors_same_datetime_and_nsv_id():
    datetime_value = datetime.now()
    dataframe = to_trr_df([
        ["id1", datetime_value, 1],
        ["id2", datetime_value, 1],
    ])
    convert_trr_data(dataframe)

def test_no_errors_same_id_and_nsv_id():
    datetime_value = datetime.now()
    dataframe = to_trr_df([
        ["id1", datetime_value, 1],
        ["id1", datetime_value+timedelta(seconds=2), 1],
    ])
    convert_trr_data(dataframe)

def test_value_error_empty():
    with pytest.raises(ValueError):
        convert_trr_data(pd.DataFrame())
from etl.validation_schemas.ligne import convert_ligne_data
from datetime import datetime, timedelta
import os
import pandas as pd
import pytest

def to_ligne_df(data):
    columns = ["ligne_id", "ligne_time", "ligne_nsv_id"]
    dataframe = pd.DataFrame(data, columns=columns).set_index("ligne_id")
    return dataframe

def test_validate_static_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dataframe = pd.read_csv(dir_path + "/../etl_test_data/ligne.csv")
    convert_ligne_data(dataframe)

def test_value_error_duplicated_primary_key():
    datetime_value = datetime.now()
    dataframe = to_ligne_df([
        ["id1", datetime_value, 3],
        ["id2", datetime_value, 1],
        ["id1", datetime_value, 1]
    ])
    with pytest.raises(ValueError):
        convert_ligne_data(dataframe)

def test_no_errors_same_datetime_and_nsv_id():
    datetime_value = datetime.now()
    dataframe = to_ligne_df([
        ["id1", datetime_value, 1],
        ["id2", datetime_value, 1],
    ])
    convert_ligne_data(dataframe)

def test_no_errors_same_id_and_nsv_id():
    datetime_value = datetime.now()
    dataframe = to_ligne_df([
        ["id1", datetime_value, 1],
        ["id1", datetime_value+timedelta(seconds=2), 1],
    ])
    convert_ligne_data(dataframe)

def test_value_error_empty():
    with pytest.raises(ValueError):
        convert_ligne_data(pd.DataFrame())
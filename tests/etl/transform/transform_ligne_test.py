from etl.transform.ligne import raw_to_pandas_ligne
import numpy as np
import os, json
from datetime import datetime
import pytest

@pytest.fixture
def raw_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/../etl_test_data/ligne.json") as file:
        return json.load(file)

def test_empty_dataframe():
    dataframe = raw_to_pandas_ligne({})
    assert len(dataframe.columns) == 3
    assert "ligne_time" in dataframe.columns
    assert "ligne_nsv_id" in dataframe.columns
    assert "ligne_id" in dataframe.columns

def test_full_dataframe(raw_data):
    dataframe = raw_to_pandas_ligne(raw_data)
    for k, v in raw_data.items():
        if(v['nsv_id']):
            df =  dataframe.loc[dataframe['ligne_id'] == k]
            assert datetime.fromtimestamp(v['time'] / 1000) == \
                df['ligne_time'].values
            assert v['nsv_id'] == df['ligne_nsv_id'].values
        else:
            assert k not in dataframe.index

def test_invalid_lines_no_errors():
    raw_data = {
        "BUL_BUL": {
            "stops": [],
            "time": 1785929005998
        },
        "C38_ABR05": {
            "nsv_id": 0,
            "time": 1785929005998
        },
        "C38_ABR06": {
            "nsv_id": 1,
            "time": 1785929005998
        },
    }
    raw_data_no_null_nsv_id = {
        "C38_ABR06": {
            "nsv_id": 1,
            "time": 1785929005998
        },
    }
    dataframe_result = raw_to_pandas_ligne(raw_data_no_null_nsv_id)
    assert np.all(dataframe_result["ligne_nsv_id"] != 0)
    assert dataframe_result.equals(raw_to_pandas_ligne(raw_data))
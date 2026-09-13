from etl.transform.trr import raw_to_pandas_trr
import numpy as np
import os, json
from datetime import datetime
import pytest

@pytest.fixture
def raw_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/../etl_test_data/trr.json") as file:
        return json.load(file)

def test_empty_dataframe():
    dataframe = raw_to_pandas_trr({})
    assert len(dataframe.columns) == 3
    assert "trr_time" in dataframe.columns
    assert "trr_nsv_id" in dataframe.columns
    assert "trr_id" in dataframe.columns

def test_full_dataframe(raw_data):
    dataframe = raw_to_pandas_trr(raw_data)
    for k, v in raw_data.items():
        v = v[0]
        if(v['nsv_id']):
            df =  dataframe.loc[dataframe['trr_id'] == k]
            assert datetime.fromtimestamp(v['time'] / 1000) == \
                df['trr_time'].values
            assert v['nsv_id'] == df['trr_nsv_id'].values
        else:
            assert k not in dataframe.index

def test_invalid_lines_no_errors():
    raw_data = {
        "N0_001": [
            {
                "nsv_id": 0,
                "time": 1785931245023
            }
        ],
        "N0_521": [
            {
                "nsv_id": 2,
                "time": 1785931250024
            }
        ],
        "N0_522": [
            {
            }
        ],
    }
    raw_data_no_null_nsv_id = {
        "N0_521": [
            {
                "nsv_id": 2,
                "time": 1785931250024
            }
        ],
    }
    dataframe_result = raw_to_pandas_trr(raw_data_no_null_nsv_id)
    assert np.all(dataframe_result["trr_nsv_id"] != 0)
    assert dataframe_result.equals(raw_to_pandas_trr(raw_data))
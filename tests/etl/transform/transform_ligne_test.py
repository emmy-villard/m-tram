from etl.transform.ligne import raw_to_pandas_ligne
import pandas as pd
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
    assert dataframe.index.name == "ligne_id"
    assert len(dataframe.columns) == 2
    assert "ligne_time" in dataframe.columns
    assert "ligne_nsv_id" in dataframe.columns

def test_full_dataframe(raw_data):
    dataframe = raw_to_pandas_ligne(raw_data)
    for k, v in raw_data.items():
        if(v['nsv_id']):
            assert datetime.fromtimestamp(v['time'] / 1000) == dataframe.loc[k]['ligne_time']
            assert v['nsv_id'] == dataframe.loc[k]['ligne_nsv_id']
        else:
            assert k not in dataframe.index
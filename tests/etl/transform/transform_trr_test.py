from etl.transform.trr import raw_to_pandas_trr
import pandas as pd
import os, json
from datetime import datetime

def test_empty_dataframe():
    dataframe = raw_to_pandas_trr({})
    assert dataframe.index.name == "trr_id"
    assert len(dataframe.columns) == 2
    assert "trr_time" in dataframe.columns
    assert "trr_nsv_id" in dataframe.columns

def test_full_dataframe():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/../etl_test_data/trr.json") as file:
        raw_data = json.load(file)
        dataframe = raw_to_pandas_trr(raw_data)
        for k, v in raw_data.items():
            v = v[0]
            if(v['nsv_id']):
                assert datetime.fromtimestamp(v['time'] / 1000) == dataframe.loc[k]['trr_time']
                assert v['nsv_id'] == dataframe.loc[k]['trr_nsv_id']
            else:
                assert k not in dataframe.index
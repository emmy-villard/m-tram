from etl.extract.ligne import fetch_ligne
from etl.transform.ligne import raw_to_pandas_ligne
from etl.extract.trr import fetch_trr
from etl.transform.trr import raw_to_pandas_trr
from etl.load.mdata_dyn import load_table

from etl.load.engine import engine
from sqlalchemy import text
from datetime import datetime
import os, json

def test_integration_ligne():
    raw_data = fetch_ligne()
    dataframe = raw_to_pandas_ligne(raw_data)
    load_table(dataframe, "ligne")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM ligne;")).all()
        assert len(result) != 0
        assert len(result) <= len(raw_data)
        for k, v in raw_data.items():
            if(v['nsv_id']):
                assert datetime.fromtimestamp(v['time'] / 1000) == dataframe.loc[k]['ligne_time']
                assert v['nsv_id'] == dataframe.loc[k]['ligne_nsv_id']
            else:
                assert k not in dataframe.index


def test_integration_trr():
    raw_data = fetch_trr()
    dataframe = raw_to_pandas_trr(raw_data)
    load_table(dataframe, "trr")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM trr;")).all()
        assert len(result) != 0
        assert len(result) <= len(raw_data)
        for k, v in raw_data.items():
            v = v[0]
            if(v['nsv_id']):
                assert datetime.fromtimestamp(v['time'] / 1000) == dataframe.loc[k]['trr_time']
                assert v['nsv_id'] == dataframe.loc[k]['trr_nsv_id']
            else:
                assert k not in dataframe.index
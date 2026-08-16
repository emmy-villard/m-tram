from etl.extract.fetch_api import fetch_api
from etl.extract.api_url import url_ligne, url_ttr
from etl.transform.ligne import raw_to_pandas_ligne
from etl.transform.trr import raw_to_pandas_trr
from orm.ligne import Ligne, NewLigneData
from orm.trr import Trr, NewTrrData
from etl.load.mdata_dyn import load_table

from sqlalchemy import text
from datetime import datetime
import os, json
from sqlalchemy.orm import Session
from orm.base import Base
from db_connection.test_engine import engine
import pytest


"""
Setup the database
"""
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
    engine.dispose()

"""
To be run on a temporary and brand new database setup
"""
def test_tables_created():
    with Session(engine) as session:
        session.execute(text("SELECT * FROM ligne;")).all()
        session.execute(text("SELECT * FROM new_ligne_data;")).all()
        session.execute(text("SELECT * FROM trr;")).all()
        session.execute(text("SELECT * FROM new_trr_data;")).all()

def test_integration_ligne():
    raw_data = fetch_api(url_ligne)
    dataframe = raw_to_pandas_ligne(raw_data)
    load_table(dataframe, engine, Ligne, NewLigneData)
    with Session(engine) as session:
        result = session.execute(text("SELECT * FROM ligne;")).all()
        assert len(result) != 0
        assert len(result) <= len(raw_data)
        for k, v in raw_data.items():
            if(v['nsv_id']):
                assert datetime.fromtimestamp(v['time'] / 1000) == dataframe.loc[k]['ligne_time']
                assert v['nsv_id'] == dataframe.loc[k]['ligne_nsv_id']
            else:
                assert k not in dataframe.index


def test_integration_trr():
    raw_data = fetch_api(url_ttr)
    dataframe = raw_to_pandas_trr(raw_data)
    load_table(dataframe, engine, Trr, NewTrrData)
    with Session(engine) as session:
        result = session.execute(text("SELECT * FROM trr;")).all()
        assert len(result) != 0
        assert len(result) <= len(raw_data)
        for k, v in raw_data.items():
            v = v[0]
            if(v['nsv_id']):
                assert datetime.fromtimestamp(v['time'] / 1000) == dataframe.loc[k]['trr_time']
                assert v['nsv_id'] == dataframe.loc[k]['trr_nsv_id']
            else:
                assert k not in dataframe.index
from etl.extract.fetch_api import fetch_api
from etl.extract.api_url import url_ligne, url_trr
from etl.transform.ligne import raw_to_pandas_ligne
from etl.transform.trr import raw_to_pandas_trr
from orm.ligne import Ligne
from orm.trr import Trr
from etl.load.mdata_dyn import load_table
from etl.validation_schemas.ligne import convert_ligne_data
from etl.validation_schemas.trr import convert_trr_data

from unittest.mock import patch, MagicMock
from sqlalchemy import text
from datetime import datetime
from sqlalchemy.orm import Session
from orm.base import Base
from db_connection.test_engine import engine
import pytest
import pandas as pd

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

@pytest.fixture()
def dataframe():
    raw_data = fetch_api(url_trr)
    dataframe = raw_to_pandas_trr(raw_data)
    return dataframe

@pytest.fixture
def mock_converter():
    return MagicMock()

"""
To be run on a temporary and brand new database setup
"""
def test_tables_created():
    with Session(engine) as session:
        session.execute(text("SELECT * FROM ligne;")).all()
        session.execute(text("SELECT * FROM trr;")).all()

def test_integration_ligne():
    raw_data = fetch_api(url_ligne)
    dataframe = raw_to_pandas_ligne(raw_data)
    load_table(dataframe, engine, Ligne, convert_ligne_data)
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
    raw_data = fetch_api(url_trr)
    dataframe = raw_to_pandas_trr(raw_data)
    load_table(dataframe, engine, Trr, convert_trr_data)
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

@pytest.mark.parametrize("data", [[], [0, 0, 0]])
def test_not_load_unvalid_table(mock_converter, dataframe, data):
    with patch("etl.load.mdata_dyn.Session", new_callable=MagicMock) as mock_session, \
    patch("pandas.DataFrame.to_sql") as mock_sql:
        mock_sess = mock_session.return_value.__enter__.return_value
        load_table(pd.DataFrame(data), (), Trr, mock_converter)
        mock_sess.execute.assert_not_called()
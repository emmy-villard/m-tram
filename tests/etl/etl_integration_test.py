from etl.classes.Ligne import Ligne
from etl.classes.Trr import Trr
from etl.classes.OpenMeteo import OpenMeteo
from etl.transform.meteo import process_meteo_data

from unittest.mock import patch, MagicMock
from sqlalchemy import text
from datetime import datetime
from sqlalchemy.orm import Session
from orm.base import Base
from db_connection.test_engine import engine
import pytest
import pandas as pd
import numpy as np

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
    raw_data = Trr.fetch(Trr.get_url())
    dataframe = Trr.raw_data_to_df(raw_data)
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
        session.execute(text("SELECT * FROM openmeteo;")).all()

def test_integration_ligne():
    raw_data = Ligne.fetch(Ligne.get_url())
    dataframe = Ligne.raw_data_to_df(raw_data)
    for k, v in raw_data.items():
        if(v['nsv_id']):
            assert datetime.fromtimestamp(v['time'] / 1000) == dataframe.loc[k]['ligne_time']
            assert v['nsv_id'] == dataframe.loc[k]['ligne_nsv_id']
        else:
            assert k not in dataframe.index
    Ligne.load_table(dataframe, engine, Ligne.orm_class(), Ligne.data_validator())
    with Session(engine) as session:
        result = session.execute(text("SELECT * FROM ligne;")).all()
        assert len(result) != 0
        assert len(result) <= len(raw_data)
        dataframe = dataframe.reset_index()
        result_df = pd.DataFrame(list(result), columns=dataframe.columns)
        assert result_df.equals(dataframe)

def test_integration_trr():
    raw_data = Trr.fetch(Trr.get_url())
    dataframe = Trr.raw_data_to_df(raw_data)
    for k, v in raw_data.items():
        v = v[0]
        if(v['nsv_id']):
            assert datetime.fromtimestamp(v['time'] / 1000) == dataframe.loc[k]['trr_time']
            assert v['nsv_id'] == dataframe.loc[k]['trr_nsv_id']
        else:
            assert k not in dataframe.index
    Trr.load_table(dataframe, engine, Trr.orm_class(), Trr.data_validator())
    with Session(engine) as session:
        result = session.execute(text("SELECT * FROM trr;")).all()
        assert len(result) != 0
        assert len(result) <= len(raw_data)
        dataframe = dataframe.reset_index()
        result_df = pd.DataFrame(list(result), columns=dataframe.columns)
        assert result_df.equals(dataframe)

def test_integration_openmeteo():
    raw_data = OpenMeteo.fetch(OpenMeteo.get_url())
    dataframe = OpenMeteo.raw_data_to_df(raw_data).reset_index()
    for k, v in raw_data["hourly"].items():
        values = np.asarray([process_meteo_data(k, val) for val in v])
        assert np.all(np.equal(dataframe[k].values, values))
    OpenMeteo.load_table(dataframe, engine, OpenMeteo.orm_class(), OpenMeteo.data_validator())
    with Session(engine) as session:
        result = session.execute(text("SELECT * FROM openmeteo;")).all()
        assert len(result) != 0
        assert len(result) == len(raw_data["hourly"]["time"])
        result_df = pd.DataFrame(list(result), columns=dataframe.columns)
        assert result_df.equals(dataframe)

@pytest.mark.parametrize("data", [[], [0, 0, 0]])
def test_not_load_unvalid_table(mock_converter, dataframe, data):
    with patch("etl.load.save_in_db.Session", new_callable=MagicMock) as mock_session, \
    patch("pandas.DataFrame.to_sql") as mock_sql:
        mock_sess = mock_session.return_value.__enter__.return_value
        Trr.load_table(pd.DataFrame(data), (), Trr.orm_class(), mock_converter)
        mock_sess.execute.assert_not_called()
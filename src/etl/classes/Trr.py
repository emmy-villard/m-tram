from etl.classes.Data import Data
from etl.extract.endpoint_url.mdata_trr import get_url as trr_url
from etl.extract.fetch_api import fetch_api
from etl.transform.trr import raw_to_pandas_trr
from etl.load.save_in_db import load_table
from db_connection.engine import engine
from orm.trr import Trr as TrrOrmClass
from etl.validation_schemas.trr import validate_trr_data

class Trr(Data):
    @staticmethod
    def get_url():
        return trr_url()

    @staticmethod
    def fetch(url):
        return fetch_api(url)

    @staticmethod
    def raw_data_to_df(raw_data):
        return raw_to_pandas_trr(raw_data)

    @staticmethod
    def load_table(dataframe, engine, orm_class, data_validator):
        load_table(dataframe, engine, orm_class, data_validator)

    @staticmethod
    def engine():
        return engine

    @staticmethod
    def orm_class():
        return TrrOrmClass

    @staticmethod
    def data_validator():
        return validate_trr_data
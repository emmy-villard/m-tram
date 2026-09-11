from etl.classes.Data import Data
from etl.extract.endpoint_url.atmo import get_url as atmo_url
from etl.extract.fetch_api import fetch_api
from etl.transform.atmo import raw_to_pandas_atmo
from etl.load.save_in_db import load_table
from db_connection.engine import engine
from orm.atmo import Atmo as AtmoOrmClass
from etl.validation_schemas.atmo import validate_atmo_data

class Atmo(Data):
    @staticmethod
    def get_url():
        return atmo_url()

    @staticmethod
    def fetch(url):
        return fetch_api(url)

    @staticmethod
    def raw_data_to_df(raw_data):
        return raw_to_pandas_atmo(raw_data)

    @staticmethod
    def load_table(dataframe, engine, orm_class, data_validator):
        load_table(dataframe, engine, orm_class, data_validator)

    @staticmethod
    def engine():
        return engine

    @staticmethod
    def orm_class():
        return AtmoOrmClass

    @staticmethod
    def data_validator():
        return validate_atmo_data

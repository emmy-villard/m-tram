from etl.classes.Data import Data
from etl.extract.endpoint_url.openmeteo import get_url as openmeteo_url
from etl.extract.fetch_api import fetch_api
from etl.transform.meteo import raw_to_pandas_meteo
from etl.load.save_in_db import load_table
from db_connection.engine import engine
from orm.openmeteo import OpenMeto as OpenMeteoOrmClass
from etl.validation_schemas.openmeteo import convert_openmeteo_data

class OpenMeteo(Data):
    @staticmethod
    def get_url(*args):
        return openmeteo_url(*args)

    @staticmethod
    def fetch(url):
        return fetch_api(url)

    @staticmethod
    def raw_data_to_df(raw_data):
        return raw_to_pandas_meteo(raw_data)

    @staticmethod
    def load_table(dataframe, engine, orm_class, data_validator):
        load_table(dataframe, engine, orm_class, data_validator)

    @staticmethod
    def engine():
        return engine

    @staticmethod
    def orm_class():
        return OpenMeteoOrmClass

    @staticmethod
    def data_validator():
        return convert_openmeteo_data

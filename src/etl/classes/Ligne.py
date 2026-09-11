from etl.classes.Data import Data
from etl.extract.endpoint_url.mdata_ligne import get_url as ligne_url
from etl.extract.fetch_api import fetch_api
from etl.transform.ligne import raw_to_pandas_ligne
from etl.load.save_in_db import load_table
from db_connection.engine import engine
from orm.ligne import Ligne as LigneOrmClass
from etl.validation_schemas.ligne import validate_ligne_data

class Ligne(Data):
    @staticmethod
    def get_url():
        return ligne_url()

    @staticmethod
    def fetch(url):
        return fetch_api(url)

    @staticmethod
    def raw_data_to_df(raw_data):
        return raw_to_pandas_ligne(raw_data)

    @staticmethod
    def load_table(dataframe, engine, orm_class, data_validator):
        load_table(dataframe, engine, orm_class, data_validator)

    @staticmethod
    def engine():
        return engine

    @staticmethod
    def orm_class():
        return LigneOrmClass

    @staticmethod
    def data_validator():
        return validate_ligne_data

from airflow.sdk import dag, task
from datetime import datetime, timedelta

from etl.extract.api_url import url_trr
from etl.extract.fetch_api import fetch_api
from etl.transform.trr import raw_to_pandas_trr
from etl.load.mdata_dyn import load_table
from db_connection.engine import engine
from orm.trr import Trr
from etl.validation_schemas.trr import convert_trr_data

@dag(
    schedule="*/5 * * * *",
    start_date=datetime(2026, 1, 1),
    description=__doc__,
    tags=["etl", "trr", "mdata", "mdata-dyn"],
    max_consecutive_failed_dag_runs=300,
    default_args={
        "retries": 5,
        "retry_delay": timedelta(minutes=2),
    },
    max_active_runs=1,
)
def etl_trr():
    """
    Extract, transform and load data from API to database
    """
    @task
    def extract_trr():
        return fetch_api(url_trr)
    
    @task
    def transform_trr(raw_data):
        return raw_to_pandas_trr(raw_data)
    
    @task
    def load_trr(dataframe):
        return load_table(dataframe, engine, Trr, convert_trr_data)

    raw_data = extract_trr()
    dataframe = transform_trr(raw_data)
    load_trr(dataframe)

etl_trr()
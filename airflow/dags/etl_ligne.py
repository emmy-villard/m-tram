from airflow.sdk import dag, task
from datetime import datetime, timedelta

from etl.extract.api_url import url_ligne
from etl.extract.fetch_api import fetch_api
from etl.transform.ligne import raw_to_pandas_ligne
from etl.load.mdata_dyn import load_table
from db_connection.engine import engine
from orm.ligne import Ligne
from etl.validation_schemas.ligne import convert_ligne_data

@dag(
    schedule="*/5 * * * *",
    start_date=datetime(2026, 1, 1),
    description=__doc__,
    tags=["etl", "ligne", "mdata", "mdata-dyn"],
    max_consecutive_failed_dag_runs=300,
    default_args={
        "retries": 5,
        "retry_delay": timedelta(minutes=2),
    },
    max_active_runs=1,
)
def etl_ligne():
    """
    Extract, transform and load data from API to database
    """
    @task
    def extract_ligne():
        return fetch_api(url_ligne)
    
    @task
    def transform_ligne(raw_data):
        return raw_to_pandas_ligne(raw_data)
    
    @task
    def load_ligne(dataframe):
        return load_table(dataframe, engine, Ligne, convert_ligne_data)

    raw_data = extract_ligne()
    dataframe = transform_ligne(raw_data)
    load_ligne(dataframe)

etl_ligne()
from airflow.sdk import dag, task
from datetime import datetime, timedelta

from etl.classes.Trr import Trr

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
        url = Trr.get_url()
        return Trr.fetch(url)
    
    @task
    def transform_trr(raw_data):
        return Trr.raw_data_to_df(raw_data)
    
    @task
    def load_trr(dataframe):
        engine = Trr.engine()
        data_validator = Trr.data_validator()
        TrrOrmClass = Trr.orm_class()
        Trr.load_table(dataframe, engine, TrrOrmClass, data_validator)

    raw_data = extract_trr()
    dataframe = transform_trr(raw_data)
    load_trr(dataframe)

etl_trr()
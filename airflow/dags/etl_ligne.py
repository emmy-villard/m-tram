from airflow.sdk import dag, task
from datetime import datetime, timedelta
from etl.classes.Ligne import Ligne

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
        url = Ligne.get_url()
        return Ligne.fetch(url)
    
    @task
    def transform_ligne(raw_data):
        return Ligne.raw_data_to_df(raw_data)
    
    @task
    def load_ligne(dataframe):
        engine = Ligne.engine()
        data_validator = Ligne.data_validator()
        LigneOrmClass = Ligne.orm_class()
        Ligne.load_table(dataframe, engine, LigneOrmClass, data_validator)

    raw_data = extract_ligne()
    dataframe = transform_ligne(raw_data)
    load_ligne(dataframe)

etl_ligne()
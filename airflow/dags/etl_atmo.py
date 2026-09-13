from airflow.sdk import dag, task, get_current_context
from datetime import datetime, timedelta
import logging

from etl.classes.Atmo import Atmo
from util.date import date_format

@dag(
    schedule="0 12 * * *",
    start_date=datetime(2026, 1, 1),
    description=__doc__,
    tags=["etl", "atmo"],
    max_consecutive_failed_dag_runs=300,
    default_args={
        "retries": 5,
        "retry_delay": timedelta(minutes=2),
    },
    max_active_runs=1,
)
def etl_atmo():
    """
    Extract, transform and load data from API to database

    Can be used in CLI to recover past data. CLI usage:
    airflow dags trigger etl_atmo --conf '{"date":"2026-01-01", "get_range_of_days":"1"}'
    date format: YYYY-MM-DD
    """

    @task
    def recover_args():
        ctx = get_current_context()
        dag_run = ctx.get("dag_run")
        if (not dag_run):
            raise ValueError("dag run context empty")

        yesterday = datetime.now() - timedelta(days=1)
        
        conf = dag_run.conf
        if (not conf):
            return {"date": yesterday, "get_range_of_days": False}
        date = conf.get("date")
        get_range_of_days = conf.get("get_range_of_days")
        if date:
            date = datetime.strptime(date, date_format())
        get_range_of_days = (get_range_of_days == "1")
        
        logging.info("date=%s get_range_of_days=%s", date, get_range_of_days)
        return {"date": date, "get_range_of_days": get_range_of_days}

    @task
    def extract_amto(args):
        date, get_range_of_days = args["date"], args["get_range_of_days"]
        url = Atmo.get_url(date, get_range_of_days)
        return Atmo.fetch(url)
    
    @task
    def transform_atmo(raw_data):
        return Atmo.raw_data_to_df(raw_data)
    
    @task
    def load_atmo(dataframe):
        engine = Atmo.engine()
        data_validator = Atmo.data_validator()
        OpenMeteoOrmClass = Atmo.orm_class()
        Atmo.load_table(dataframe, engine, OpenMeteoOrmClass, data_validator)

    args = recover_args()
    raw_data = extract_amto(args)
    dataframe = transform_atmo(raw_data)
    load_atmo(dataframe)

etl_atmo()

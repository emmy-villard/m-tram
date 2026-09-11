from airflow.sdk import dag, task, get_current_context
from datetime import datetime, timedelta
import logging

from etl.classes.OpenMeteo import OpenMeteo
from util.date import date_format

@dag(
    schedule="0 12 * * *",
    start_date=datetime(2026, 1, 1),
    description=__doc__,
    tags=["etl", "openmeteo"],
    max_consecutive_failed_dag_runs=300,
    default_args={
        "retries": 5,
        "retry_delay": timedelta(minutes=2),
    },
    max_active_runs=1,
)
def etl_meteo():
    """
    Extract, transform and load data from API to database

    Can be used in CLI to recover past data. CLI usage:
    airflow dags trigger recover_past_data --conf '{"start_date":"2026-01-01", "end_date":"2026-01-07"}'
    date format: YYYY-MM-DD
    start_date and end_date both included
    """

    @task
    def recover_dates():
        ctx = get_current_context()
        dag_run = ctx.get("dag_run")
        if (not dag_run):
            raise ValueError("dag run context empty")

        yesterday = datetime.now() - timedelta(days=1)
        start_date, end_date = yesterday, yesterday
        
        conf = dag_run.conf
        if (not conf):
            return {"start_date": start_date, "end_date": end_date}
        start_date_str = conf.get("start_date")
        end_date_str = conf.get("end_date")
        if start_date_str:
            start_date = datetime.strptime(start_date_str, date_format())
        if end_date_str:
            end_date = datetime.strptime(end_date_str, date_format())

        numdays = (end_date - start_date).days
        if numdays < 0:
            raise ValueError("start_date must be before end_date")
        
        logging.info("start_date=%s end_date=%s", start_date, end_date)

        return {"start_date": start_date, "end_date": end_date}

    @task
    def extract_openmeteo(dates):
        start_date, end_date = dates["start_date"], dates["end_date"]
        url = OpenMeteo.get_url(start_date, end_date)
        return OpenMeteo.fetch(url)
    
    @task
    def transform_openmeteo(raw_data):
        return OpenMeteo.raw_data_to_df(raw_data)
    
    @task
    def load_openmeteo(dataframe):
        engine = OpenMeteo.engine()
        data_validator = OpenMeteo.data_validator()
        OpenMeteoOrmClass = OpenMeteo.orm_class()
        OpenMeteo.load_table(dataframe, engine, OpenMeteoOrmClass, data_validator)

    dates = recover_dates()
    raw_data = extract_openmeteo(dates)
    dataframe = transform_openmeteo(raw_data)
    load_openmeteo(dataframe)

etl_meteo()

from airflow.sdk import dag, task, get_current_context
from datetime import datetime, timedelta
import logging

from etl.extract.endpoint_url.openmeteo import get_url
from etl.extract.fetch_api import fetch_api
from etl.transform.meteo import raw_to_pandas_meteo
from etl.load.save_in_db import load_table
from db_connection.engine import engine
from orm.openmeteo import OpenMeto
from etl.validation_schemas.openmeteo import convert_openmeteo_data
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
        return fetch_api(get_url(start_date, end_date))
    
    @task
    def transform_openmeteo(raw_data):
        return raw_to_pandas_meteo(raw_data)
    
    @task
    def load_openmeteo(dataframe):
        load_table(dataframe, engine, OpenMeto, convert_openmeteo_data)

    dates = recover_dates()
    raw_data = extract_openmeteo(dates)
    dataframe = transform_openmeteo(raw_data)
    load_openmeteo(dataframe)

etl_meteo()

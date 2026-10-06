from airflow.sdk import dag, task
from datetime import datetime, timedelta

from db_connection.engine import engine
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
import etl.extract.aggregation_table as aggregation_table
from orm.hourlyagg import HourlyAggregate
import logging

@dag(
    schedule="0 13 * * *",
    start_date=datetime(2026, 1, 1),
    description=__doc__,
    tags=[
        "hourly_aggregate",
        "ligne", "trr", "mdata", "mdata-dyn",
        "openmeteo",
        "atmo",
    ],
    max_consecutive_failed_dag_runs=10,
    default_args={
        "retries": 5,
        "retry_delay": timedelta(minutes=2),
    },  
    max_active_runs=1,
)
def increment_aggregate_table():
    """
    Add data from yesterday to aggregate table
    """
    @task
    def insert_new_line():
        yesterday = datetime.now() - timedelta(days=1)
        agg_select_stmt = aggregation_table.get_select_stmt(yesterday)
        with Session(engine) as session:
            upsert_stmt = insert(HourlyAggregate).from_select(
                    aggregation_table.get_columns(),
                    agg_select_stmt
            ).on_conflict_do_nothing()
            result_proxy = session.execute(upsert_stmt)
            session.commit()
            logging.info(f"Add aggregate table line for {yesterday}\n \
                {result_proxy}")

    insert_new_line()

increment_aggregate_table()

from airflow.sdk import dag, task
from datetime import datetime, timedelta

from db_connection.engine import engine
from sqlalchemy.orm import Session
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
import etl.extract.aggregation_table as aggregation_table
from orm.hourlyagg import HourlyAggregate
import logging

@dag(
    schedule=None,
    start_date=datetime(2026, 1, 1),
    description=__doc__,
    tags=[
        "hourly_aggregate",
        "ligne", "trr", "mdata", "mdata-dyn",
        "openmeteo",
        "atmo",
    ],
    max_consecutive_failed_dag_runs=3,
    default_args={
        "retries": 5,
        "retry_delay": timedelta(minutes=2),
    },
    max_active_runs=1,
)
def remake_aggregate_table():
    """
    Remake the whole aggregate table
    """
    @task
    def remake_table():
        agg_select_stmt = aggregation_table.get_select_stmt(None)
        with Session(engine) as session:
            insert_stmt = insert(HourlyAggregate).from_select(
                    aggregation_table.get_columns(),
                    agg_select_stmt
            )
            drop_table_stmt = delete(HourlyAggregate) # Drop all lines

            result_proxy = session.execute(drop_table_stmt) 
            result_proxy = session.execute(insert_stmt)
            session.commit()
            logging.info(f"Remake whole aggregate table\n \
                {result_proxy}")

    remake_table()

remake_aggregate_table()

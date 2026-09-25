from sqlalchemy import select
from sqlalchemy.sql.expression import between
from sqlalchemy.orm import Session
from db_connection.engine import engine
from datetime import datetime, timedelta

from orm.hourlyagg import HourlyAggregate


db_starting_date = datetime(day=26, month=8, year=2026)

AGGREGATE_PERIOD_TIMEDELTA = {
    "last_week": timedelta(weeks=1), # 1 week
    "last_month": timedelta(days=30), # 1 month
    "last_three_months": timedelta(days=90), # 3 months
    "last_year": timedelta(days=365), # 1 year
    "all_time": timedelta(days=365*1000), # 1000 years
}


def _get_start_end_date(aggregate_period: str):
    if aggregate_period not in AGGREGATE_PERIOD_TIMEDELTA:
        raise ValueError(f"Unvalid aggregate period: {aggregate_period} \
            Please choose between {AGGREGATE_PERIOD_TIMEDELTA.keys()}"
        )
    end_of_yesterday = datetime.now().replace(
        hour=23, minute=59, second=59, microsecond=999999
    ) - timedelta(days=1)
    start_date = max(
        end_of_yesterday - AGGREGATE_PERIOD_TIMEDELTA[aggregate_period],
        db_starting_date
    ).replace(hour=0, minute=0, second=0, microsecond=0)
    return start_date, end_of_yesterday

def get_data(table_name: str):
    start_date, end_date = _get_start_end_date(table_name)
    table = HourlyAggregate.__table__
    with Session(engine) as session:
        select_stmt = select(HourlyAggregate).where(between(
            table.c.hour_start,
            start_date,
            end_date)
        )
        return session.execute(select_stmt).scalars().all()
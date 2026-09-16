from sqlalchemy import select
from sqlalchemy.orm import Session

from db_connection.engine import engine
from orm.trr import Trr


def get_raw_data():
    with Session(engine) as session:
        trr_data = session.scalars(select(Trr)).all()

        return [
            {
                "trr_id": trr.trr_id,
                "trr_time": trr.trr_time,
                "trr_nsv_id": trr.trr_nsv_id,
            }
            for trr in trr_data
        ]

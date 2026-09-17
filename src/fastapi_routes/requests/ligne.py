from db_connection.engine import engine
from sqlalchemy.orm import Session

from sqlalchemy import select
from orm.ligne import Ligne

def get_raw_data():
    with Session(engine) as session:
        select_stmt = select(Ligne)
        lines = session.execute(select_stmt).scalars().all()
        return [
            {
                "ligne_id": line.ligne_id,
                "ligne_time": line.ligne_time,
                "ligne_nsv_id": line.ligne_nsv_id,
            }
            for line in lines
        ]
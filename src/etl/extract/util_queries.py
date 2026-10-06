from datetime import datetime
from typing import Sequence
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy import select, func

from db_connection.engine import engine
from orm.ligne import Ligne 
from orm.trr import Trr
from orm.openmeteo import OpenMeto
from orm.atmo import Atmo


TIME_COLUMN_BY_MODEL = {
    Ligne : Ligne.__table__.c.ligne_time,
    Trr : Trr.__table__.c.trr_time,
    OpenMeto : OpenMeto.__table__.c.time,
    Atmo : Atmo.__table__.c.time,
}

def get_earliest_date_in_db(tables: Sequence[type[DeclarativeBase]] = [
    Ligne, Trr, OpenMeto, Atmo
]) -> datetime:
    lowest_times = []
    with Session(engine) as session:
        for table in tables:
            select_stmt = select(func.min(TIME_COLUMN_BY_MODEL[table])
                ).select_from(table)
            min_time = session.execute(select_stmt).scalar_one()
            if min_time != None:
                lowest_times.append(min_time)
    return min(lowest_times)
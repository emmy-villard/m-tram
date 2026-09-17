from db_connection.engine import engine
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy import select, func
from typing import Sequence

from orm.ligne import Ligne 
from orm.trr import Trr
from orm.openmeteo import OpenMeto
from orm.atmo import Atmo

def get_data(tables: Sequence[type[DeclarativeBase]] = [
    Ligne, Trr, OpenMeto, Atmo
]):
    count = dict()
    with Session(engine) as session:
        for table in tables:
            select_stmt = select(func.count().label("count")).select_from(table)
            line_count = session.execute(select_stmt).scalar_one()
            count[table.__tablename__] = line_count
    return count
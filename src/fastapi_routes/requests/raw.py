from sqlalchemy import select
from sqlalchemy.orm import Session, DeclarativeBase

from db_connection.engine import engine
from orm.atmo import Atmo

def get_data(table: type[DeclarativeBase]):
    with Session(engine) as session:
        row_data = session.scalars(select(table)).all()
        return row_data
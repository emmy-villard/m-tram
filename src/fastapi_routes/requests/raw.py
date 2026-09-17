from sqlalchemy import select
from sqlalchemy.orm import Session, DeclarativeBase
from db_connection.engine import engine

def get_data(table: type[DeclarativeBase]):
    with Session(engine) as session:
        select_stmt = select(table)
        row_data = session.execute(select_stmt).scalars().all()
        return row_data
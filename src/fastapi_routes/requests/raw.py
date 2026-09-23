from sqlalchemy import select, func
from sqlalchemy.orm import Session
from db_connection.engine import engine

from orm.ligne import Ligne
from orm.trr import Trr
from orm.openmeteo import OpenMeto
from orm.atmo import Atmo

from fastapi.responses import StreamingResponse

MODEL_REGISTRY = {
    "ligne": Ligne,
    "trr": Trr,
    "openmeteo": OpenMeto,
    "atmo": Atmo,
}


def _get_model(table_name: str):
    if table_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown table: {table_name}")
    return MODEL_REGISTRY[table_name]


def get_data(table_name: str):
    table = _get_model(table_name)
    with Session(engine) as session:
        count_stmt = select(func.count().label("count")).select_from(table)
        line_count = session.execute(count_stmt).scalar_one()
        if line_count > 100000: #More than 100k lines
            return stream_csv(table)
        select_stmt = select(table)
        return session.execute(select_stmt).scalars().all()

def stream_csv(table):
    columns = list(table.__table__.columns.keys())

    def row_generator():
        yield ",".join(columns) + "\n"
        with Session(engine) as session:
            select_stmt = select(table)
            rows = session.execute(select_stmt).scalars().all()
            for row in rows:
                yield ",".join(str(getattr(row, column)) for column in columns) + "\n"

    return StreamingResponse(row_generator(), media_type="text/csv")
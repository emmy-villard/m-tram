from sqlalchemy import select
from sqlalchemy.orm import Session
from db_connection.engine import engine

from orm.ligne import Ligne 
from orm.trr import Trr
from orm.openmeteo import OpenMeto
from orm.atmo import Atmo

MODEL_REGISTRY = {
    "ligne": Ligne,
    "trr": Trr,
    "openmeteo": OpenMeto,
    "atmo": Atmo,
}

def get_data(table_name: str):
    with Session(engine) as session:
        select_stmt = select(MODEL_REGISTRY[table_name])
        row_data = session.execute(select_stmt).scalars().all()
        return row_data
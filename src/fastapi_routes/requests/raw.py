from sqlalchemy import select, func
from sqlalchemy.orm import Session
from db_connection.engine import engine

from orm.ligne import Ligne
from orm.trr import Trr
from orm.openmeteo import OpenMeto
from orm.atmo import Atmo

import io, csv

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
    # Disable nginx proxy buffering, otherwise the reverse proxy accumulates the
    # whole body before forwarding it, so the client sees an empty file until timeout.
    headers = {"X-Accel-Buffering": "no"}
    return StreamingResponse(_row_generator(table), media_type="text/csv", headers=headers)



def _row_generator(table):
    columns = list(table.__table__.columns.keys())
    header_buf = io.StringIO()
    writer = csv.writer(header_buf)

    writer.writerow(columns)
    yield header_buf.getvalue()

    with Session(engine) as session:
        TARGET_CHUNK_BYTES = 512 * 1024  # 512 kB
        YIELD_PER = 50_000

        select_stmt = select(table).execution_options(
            stream_results=True, yield_per=YIELD_PER
        )
        buffer = io.StringIO()
        writer = csv.writer(buffer)

        for row in session.execute(select_stmt).scalars():
            writer.writerow([getattr(row, c) for c in columns])

            if buffer.tell() >= TARGET_CHUNK_BYTES:
                yield buffer.getvalue()
                buffer.seek(0)
                buffer.truncate(0)

        if buffer.tell():  # Last lines not returned
            yield buffer.getvalue()
        buffer.close()
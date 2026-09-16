from sqlalchemy import select
from sqlalchemy.orm import Session

from db_connection.engine import engine
from orm.atmo import Atmo


def get_raw_data():
    with Session(engine) as session:
        atmo_data = session.scalars(select(Atmo)).all()

        return [
            {
                "time": atmo.time,
                "pollution_index": atmo.pollution_index,
                "is_value_mesured": atmo.is_value_mesured,
                "PM10_index": atmo.PM10_index,
                "PM2_5_index": atmo.PM2_5_index,
                "O3_index": atmo.O3_index,
                "NO2_index": atmo.NO2_index,
                "SO2_index": atmo.SO2_index,
            }
            for atmo in atmo_data
        ]

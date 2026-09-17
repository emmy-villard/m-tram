from sqlalchemy import select
from sqlalchemy.orm import Session

from db_connection.engine import engine
from orm.openmeteo import OpenMeto


def get_raw_data():
    with Session(engine) as session:
        openmeteo_data = session.scalars(select(OpenMeto)).all()

        return [
            {
                "time": weather.time,
                "temperature_2m": weather.temperature_2m,
                "apparent_temperature": weather.apparent_temperature,
                "relativehumidity_2m": weather.relativehumidity_2m,
                "precipitation": weather.precipitation,
                "rain": weather.rain,
                "snowfall": weather.snowfall,
                "weathercode": weather.weathercode,
                "pressure_msl": weather.pressure_msl,
                "cloudcover": weather.cloudcover,
                "windspeed_10m": weather.windspeed_10m,
                "windgusts_10m": weather.windgusts_10m,
            }
            for weather in openmeteo_data
        ]

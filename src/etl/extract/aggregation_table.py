from datetime import datetime, timedelta
from sqlalchemy import select, func, between, true

from etl.classes.Trr import Trr
from etl.classes.Ligne import Ligne
from etl.classes.Atmo import Atmo
from etl.classes.OpenMeteo import OpenMeteo

from etl.extract.util_queries import get_earliest_date_in_db

def get_select_stmt(date: datetime|None):
    """
    Returns a select statement for a given day
    """
    # Setup dates
    start_date: datetime
    end_date: datetime
    if date is None:
        start_date = get_earliest_date_in_db()
        yesterday = datetime.now() - timedelta(days=1)
        end_date = yesterday.replace(
            hour=23, minute=59, second=59, microsecond=999999
        )
    else:
        end_date = date.replace(
            hour=23, minute=59, second=59, microsecond=999999
        )
        start_date = end_date.replace(
            hour=0, minute=0, second=0, microsecond=0
        )

    # Table "ligne"
    ligne_table = Ligne.orm_class().__table__
    ligne_time_col = ligne_table.c.ligne_time
    ligne_traffic_level_col = ligne_table.c.ligne_nsv_id
    ligne_hours_col = func.date_trunc(
        'hour',
        ligne_time_col
    ).label('hour')
    ligne_agg = select(
        ligne_hours_col,
        func.avg(ligne_traffic_level_col).label('mean_tram_traffic')
    ).select_from(
        ligne_table
    ).where(
        between(
            ligne_time_col,
            start_date,
            end_date
        )
    ).group_by(ligne_hours_col
    ).cte('ligne_agg')

    # Table "trr"
    trr_table = Trr.orm_class().__table__
    trr_time_col = trr_table.c.trr_time
    trr_traffic_level_col = trr_table.c.trr_nsv_id
    trr_hours_col = func.date_trunc(
        'hour',
        trr_time_col
    ).label('hour')
    trr_agg = select(
        trr_hours_col,
        func.avg(trr_traffic_level_col).label('mean_road_traffic')
    ).select_from(
        trr_table
    ).where(
        between(
            trr_time_col,
            start_date,
            end_date
        )
    ).group_by(trr_hours_col
    ).cte('trr_agg')

    # Table "atmo"
    atmo_table = Atmo.orm_class().__table__
    atmo_cols = atmo_table.c
    atmo_agg = select(
        func.avg(atmo_cols.pollution_index).label('mean_pollution_index'),
        func.avg(atmo_cols.PM10_index).label('mean_PM10_pollution_index'),
        func.avg(atmo_cols.PM2_5_index).label('mean_PM2_5_pollution_index'),
        func.avg(atmo_cols.O3_index).label('mean_O3_pollution_index'),
        func.avg(atmo_cols.NO2_index).label('mean_NO2_pollution_index'),
        func.avg(atmo_cols.SO2_index).label('mean_SO2_pollution_index')
    ).select_from(
        atmo_table
    ).where(
        between(
            atmo_cols.time,
            start_date,
            end_date
        )
    ).cte('atmo_agg')

    # Table "openmeteo"
    openmeteo_table = OpenMeteo.orm_class().__table__
    meteo_cols = openmeteo_table.c
    meteo_hours_col = func.date_trunc(
        'hour',
        meteo_cols.time
    ).label('hour')
    openmeteo_agg = select(
        meteo_hours_col,
        func.avg(meteo_cols.temperature_2m).label('mean_temperature'),
        func.sum(meteo_cols.precipitation).label('precipitation_1h'),
        func.sum(meteo_cols.rain).label('rain_1h'),
        func.avg(meteo_cols.relativehumidity_2m).label('relative_humidity'),
        func.avg(meteo_cols.cloudcover).label('mean_cloud_cover'),
        func.avg(meteo_cols.windspeed_10m).label('mean_wind_speed')
    ).select_from(
        openmeteo_table
    ).where(
        between(
            meteo_cols.time,
            start_date,
            end_date
        )
    ).group_by(meteo_hours_col
    ).cte('openmeteo_agg')

    # Joins
    join_clause = (
        openmeteo_agg
        .outerjoin(
            ligne_agg,
            openmeteo_agg.c.hour == ligne_agg.c.hour
        )
        .outerjoin(
            trr_agg,
            openmeteo_agg.c.hour == trr_agg.c.hour
        )
        .join(
            atmo_agg,
            true() # No conditions (cross join)
        )
    )

    stmt = select(
        openmeteo_agg.c.hour,
        ligne_agg.c.mean_tram_traffic,
        trr_agg.c.mean_road_traffic,
        atmo_agg.c.mean_pollution_index,
        atmo_agg.c.mean_PM10_pollution_index,
        atmo_agg.c.mean_PM2_5_pollution_index,
        atmo_agg.c.mean_O3_pollution_index,
        atmo_agg.c.mean_NO2_pollution_index,
        atmo_agg.c.mean_SO2_pollution_index,
        openmeteo_agg.c.mean_temperature,
        openmeteo_agg.c.precipitation_1h,
        openmeteo_agg.c.rain_1h,
        openmeteo_agg.c.relative_humidity,
        openmeteo_agg.c.mean_cloud_cover,
        openmeteo_agg.c.mean_wind_speed,
    ).select_from(
        join_clause
    ).order_by(
        openmeteo_agg.c.hour
    )

    return stmt

def get_columns():
    return [
        "hour",
        "mean_tram_traffic",
        "mean_road_traffic",
        "mean_pollution_index",
        "pm10_index",
        "pm2_5_index",
        "o3_index",
        "no2_index",
        "so2_index",
        "mean_temperature",
        "precipitation_total",
        "rainfall_total",
        "average_relative_humidity",
        "average_cloud_cover",
        "average_wind_speed",
    ]
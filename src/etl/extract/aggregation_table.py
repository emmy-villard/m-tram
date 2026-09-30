from datetime import datetime, timedelta
from sqlalchemy import select, func, between

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
    ).where(
        between(
            meteo_cols.time,
            start_date,
            end_date
        )
    ).group_by(meteo_hours_col
    ).cte('openmeteo_agg')

    # Joins
    #TODO
    joins = ligne_agg
    joins = trr_agg
    return joins

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

"""
SELECT
    openmeteo_agg.hour,
    ligne_agg.mean_tram_traffic,
    trr_agg.mean_road_traffic,
    atmo_agg.mean_pollution_index,
    atmo_agg.pm10_index,
    atmo_agg.pm2_5_index,
    atmo_agg.o3_index,
    atmo_agg.no2_index,
    atmo_agg.so2_index,
    openmeteo_agg.mean_temperature,
    openmeteo_agg.precipitation_total,
    openmeteo_agg.rainfall_total,
    openmeteo_agg.average_relative_humidity,
    openmeteo_agg.average_cloud_cover,
    openmeteo_agg.average_wind_speed
FROM openmeteo_agg
LEFT JOIN ligne_agg
    ON openmeteo_agg.hour = ligne_agg.hour
LEFT JOIN trr_agg
    ON openmeteo_agg.hour = trr_agg.hour
CROSS JOIN atmo_agg
ORDER BY openmeteo_agg.hour;
"""



"""
WITH ligne_agg AS (
    SELECT DATE_TRUNC('hour', ligne_time) as hour, AVG(ligne_nsv_id) as mean_tram_traffic
    FROM ligne
    WHERE ligne_time BETWEEN '2026-09-24' AND '2026-09-24 23:59:59'
    GROUP BY DATE_TRUNC('hour', ligne_time)
),
trr_agg AS (
    SELECT DATE_TRUNC('hour', trr_time) as hour, AVG(trr_nsv_id) as mean_road_traffic
    FROM trr
    WHERE trr_time BETWEEN '2026-09-24' AND '2026-09-24 23:59:59'
    GROUP BY DATE_TRUNC('hour', trr_time)
),
atmo_agg AS (
    SELECT
        AVG(pollution_index) as mean_pollution_index,
        AVG("PM10_index") as pm10_index,
        AVG("PM2_5_index") as pm2_5_index,
        AVG("O3_index") as o3_index,
        AVG("NO2_index") as no2_index,
        AVG("SO2_index") as so2_index
    FROM atmo
    WHERE time BETWEEN '2026-09-24' AND '2026-09-24 23:59:59'
),
openmeteo_agg AS (
    SELECT
        DATE_TRUNC('hour', time) as hour,
        AVG(temperature_2m) as mean_temperature,
        SUM(precipitation) as precipitation_total,
        SUM(rain) as rainfall_total,
        AVG(relativehumidity_2m) as average_relative_humidity,
        AVG(cloudcover) as average_cloud_cover,
        AVG(windspeed_10m) as average_wind_speed
    FROM openmeteo
    WHERE time BETWEEN '2026-09-24' AND '2026-09-24 23:59:59'
    GROUP BY DATE_TRUNC('hour', time)
)
SELECT
    openmeteo_agg.hour,
    ligne_agg.mean_tram_traffic,
    trr_agg.mean_road_traffic,
    atmo_agg.mean_pollution_index,
    atmo_agg.pm10_index,
    atmo_agg.pm2_5_index,
    atmo_agg.o3_index,
    atmo_agg.no2_index,
    atmo_agg.so2_index,
    openmeteo_agg.mean_temperature,
    openmeteo_agg.precipitation_total,
    openmeteo_agg.rainfall_total,
    openmeteo_agg.average_relative_humidity,
    openmeteo_agg.average_cloud_cover,
    openmeteo_agg.average_wind_speed
FROM openmeteo_agg
LEFT JOIN ligne_agg
    ON openmeteo_agg.hour = ligne_agg.hour
LEFT JOIN trr_agg
    ON openmeteo_agg.hour = trr_agg.hour
CROSS JOIN atmo_agg
ORDER BY openmeteo_agg.hour;
"""
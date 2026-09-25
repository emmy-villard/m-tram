# Database Table Schemas
This document provides the current relational schema used by the project. Schema changes are tracked with Alembic, and the test database mirrors the application database so that migrations and table structures remain consistent.

## Dynamic MData
### trr
- `trr_id`: TEXT
- `trr_time`: TIMESTAMP
- `trr_nsv_id`: INTEGER, valid range is 1 to 4
- Primary key: `(trr_id, trr_time)`

### ligne
- `ligne_id`: TEXT
- `ligne_time`: TIMESTAMP
- `ligne_nsv_id`: INTEGER, valid range is 1 to 4
- Primary key: `(ligne_id, ligne_time)`

## OpenMeteo
### openmeteo
- `time`: TIMESTAMP
- `temperature_2m`: FLOAT
- `apparent_temperature`: FLOAT
- `relativehumidity_2m`: INTEGER, range 0 to 100
- `precipitation`: FLOAT
- `rain`: FLOAT
- `snowfall`: FLOAT
- `weathercode`: INTEGER
- `pressure_msl`: FLOAT
- `cloudcover`: INTEGER, range 0 to 100
- `windspeed_10m`: FLOAT
- `windgusts_10m`: FLOAT
- Primary key: `time`

## Atmo Auvergne-Rhône-Alpes
### atmo
- `time`: TIMESTAMP
- `pollution_index`: INTEGER, valid range is 1 to 6
- `is_value_mesured`: BOOLEAN
- `PM10_index`: INTEGER, valid range is 1 to 6
- `PM2_5_index`: INTEGER, valid range is 1 to 6
- `O3_index`: INTEGER, valid range is 1 to 6
- `NO2_index`: INTEGER, valid range is 1 to 6
- `SO2_index`: INTEGER, valid range is 1 to 6
- Primary key: `time`

## Dashboard Aggregate Tables

The dashboard uses two consolidated aggregate tables populated by Airflow. The `traffic_type` value is `tram` for values derived from `ligne` and `road` for values derived from `trr`. `average_congestion_level` is the average source `nsv_id`, where `1` represents fluid traffic and `4` represents a blocked or closed situation.

### dashboard_hourly_aggregates
- `hour_start`: TIMESTAMP, start of the aggregated hour
- `traffic_type`: TEXT, `tram` or `road`
- `average_congestion_level`: FLOAT
- `pollution_index`: FLOAT
- `pm10_index`: FLOAT
- `pm2_5_index`: FLOAT
- `o3_index`: FLOAT
- `no2_index`: FLOAT
- `so2_index`: FLOAT
- `precipitation_total`: FLOAT
- `rainfall_total`: FLOAT
- `average_temperature`: FLOAT
- `average_relative_humidity`: FLOAT
- `average_cloud_cover`: FLOAT
- `average_wind_speed`: FLOAT
- Primary key: (`hour_start`, `traffic_type`)

### dashboard_two_hour_aggregates
- `hour_start`: TIMESTAMP, start timestamp of the two-hour period
- `time_block`: TEXT, predefined two-hour block identifier
- `traffic_type`: TEXT, `tram` or `road`
- `average_congestion_level`: FLOAT
- `pollution_index`: FLOAT
- `pm10_index`: FLOAT
- `pm2_5_index`: FLOAT
- `o3_index`: FLOAT
- `no2_index`: FLOAT
- `so2_index`: FLOAT
- `precipitation_total`: FLOAT
- `rainfall_total`: FLOAT
- `average_temperature`: FLOAT
- `average_relative_humidity`: FLOAT
- `average_cloud_cover`: FLOAT
- `average_wind_speed`: FLOAT
- Primary key: (`hour_start`, `time_block`, `traffic_type`)

## Dashboard Aggregate Refreshes

The dashboard aggregate tables are maintained by two Airflow DAGs:

- The **manual full-refresh DAG** rebuilds both aggregate tables for the complete available history. It is used for initial population, historical backfills, source corrections, and aggregation-logic changes.
- The **daily incremental-refresh DAG** runs at 13:00, after the daily weather and air-quality loads scheduled at 12:00. It refreshes the previous 24-hour window and updates both the hourly and affected two-hour aggregates.

Both refresh modes validate their output before writing it. The daily refresh replaces the affected time window, making reruns idempotent and allowing corrections to source data to be reflected without rebuilding the full history. The full refresh replaces the contents of both aggregate tables with the complete rebuilt history.

The daily refresh assumes that already processed source history is unchanged, that the aggregation logic has not changed, and that all source loads for the refreshed period have completed. Any correction, backfill, deletion, or reprocessing affecting an older period requires the manual full-refresh DAG.

## Notes
The main analytical tables are the time-series tables (`trr`, `ligne`, `openmeteo`, `atmo`). They are designed around a timestamp-based primary key so that historical comparison and joins are straightforward across all sources.
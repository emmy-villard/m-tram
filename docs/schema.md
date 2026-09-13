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

## Notes
The main analytical tables are the time-series tables (`trr`, `ligne`, `openmeteo`, `atmo`). They are designed around a timestamp-based primary key so that historical comparison and joins are straightforward across all sources.
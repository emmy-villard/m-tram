# FastAPI API

The API exposes the data collected by the ETL pipeline in read-only mode.

## Routes

### `GET /count`

Returns the number of rows available in each exposed table.

Example response:

```json
{
  "ligne": 123,
  "trr": 456,
  "openmeteo": 789,
  "atmo": 321
}
```

### `GET /raw/ligne`

Returns raw public transport line data.

Returned fields:

- `ligne_id`
- `ligne_time`
- `ligne_nsv_id`

### `GET /raw/trr`

Returns raw road traffic data.

Returned fields:

- `trr_id`
- `trr_time`
- `trr_nsv_id`

### `GET /raw/atmo`

Returns atmospheric pollution measurements.

Returned fields:

- `time`
- `pollution_index`
- `is_value_mesured`
- `PM10_index`
- `PM2_5_index`
- `O3_index`
- `NO2_index`
- `SO2_index`

### `GET /raw/openmeteo`

Returns Open-Meteo weather measurements.

Returned fields:

- `time`
- `temperature_2m`
- `apparent_temperature`
- `relativehumidity_2m`
- `precipitation`
- `rain`
- `snowfall`
- `weathercode`
- `pressure_msl`
- `cloudcover`
- `windspeed_10m`
- `windgusts_10m`

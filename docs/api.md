# FastAPI API

The API exposes the data collected by the ETL pipeline in read-only mode.

# Routes

## [`GET /`](/)

Returns this API documentation, including the available read-only endpoints.

## [`GET /source.md`](source.md)

Returns the documentation for the ETL data sources and ATMO pollution levels.

## [`GET /count`](count)

Returns the number of rows available in each exposed table.

Response example:

```json
{
  "ligne": 123,
  "trr": 456,
  "openmeteo": 789,
  "atmo": 321
}
```

## [`GET /raw/{data}`](raw/atmo)

Returns the raw rows from the requested table.

Path parameter:

- `data`: name of the table to query.

Available values:

- `ligne`
- `trr`
- `openmeteo`
- `atmo`

The response is a JSON array. Each item contains the columns of the selected
table. See [schema.md](schema.md) for the columns returned by each table.

## [`GET /aggregate/{aggregate_period}`](aggregate/last_week)

Returns the hourly aggregates used by the dashboard, from the
`dashboard_hourly_aggregates` table. See
[dashboard-aggregate-table.md](dashboard-aggregate-table.md) for how it is built.

Path parameter:

- `aggregate_period`: period to return, ending yesterday at 23:59:59.

Available values:

- `last_week`
- `last_month`
- `last_three_months`
- `last_year`
- `all_time`

The start date is never earlier than the first collected day (2026-08-26).
An unknown period (for example a date) returns a `404` with an explanatory message.

The response is a JSON array with one item per hour and per traffic type
(`tram` and `road`), both sharing the same environmental values:

```json
[
  {
    "hour_start": "2026-08-26T08:00:00",
    "traffic_type": "tram",
    "average_congestion_level": 0.42,
    "pollution_index": 2.0,
    "pm10_index": 2.0,
    "pm2_5_index": 2.0,
    "o3_index": 1.0,
    "no2_index": 1.0,
    "so2_index": 1.0,
    "precipitation_total": 0.0,
    "rainfall_total": 0.0,
    "average_temperature": 21.3,
    "average_relative_humidity": 64.0,
    "average_cloud_cover": 30.0,
    "average_wind_speed": 12.5
  }
]
```

The array is empty (`[]`) when the table has no rows for the period, for
example before the Airflow aggregation DAGs have run.

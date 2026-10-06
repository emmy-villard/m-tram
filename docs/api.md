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

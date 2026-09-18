# FastAPI API

The API exposes the data collected by the ETL pipeline in read-only mode.

# Routes

## [`Get /`](https://api.m-tram.emmyvillard.fr/)
Returns this document

## [`GET /count`](https://api.m-tram.emmyvillard.fr/count)

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

## [`GET /raw/{data}`](https://api.m-tram.emmyvillard.fr/ligne)

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

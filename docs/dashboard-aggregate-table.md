# Dashboard Aggregate Table

## Purpose

The dashboard requires fast access to historical congestion and environmental data. To avoid repeatedly aggregating raw time-series tables for every API request, the database stores precomputed hourly aggregates for the measurements displayed by the dashboard.

The aggregate table is intended for read-only historical analysis. FastAPI endpoints query the precomputed data and apply dashboard filters, rather than recomputing the underlying averages from the raw tables.

## Aggregate Granularity

Each aggregate record represents one completed one-hour period. The aggregation key must include:

- The start timestamp of the hour.
- The traffic type, where the value is derived from tram ("ligne") or road-traffic data ("trr").

The hourly timestamp is the common join key for congestion and weather values. Atmo supplies daily indices; the daily value is associated with every weather hour on the same date. The dashboard aggregate table definitions are documented in `schema.md`.

## Aggregate Measurements

The hourly aggregate must provide the congestion value together with the environmental variables that can be selected in the dashboard:

- Congestion for tram traffic.
- Congestion for road traffic.
- Overall air-pollution index.
- Air-pollution sub-indices: PM10, PM2.5, O3, NO2, and SO2.
- Cumulative precipitation and rainfall for the hour.
- Average temperature.
- Average relative humidity.
- Average cloud cover.
- Average wind speed.

The source tables are `trr`, `ligne`, `openmeteo`, and `atmo`.

## Refresh Strategies

The aggregate table is refreshed through two separate Airflow DAGs:

- A **manual full-refresh DAG** recalculates the complete hourly aggregate from all available raw source data. It is intended for initial population, source corrections, backfills, and changes to the aggregation logic.
- A **daily incremental-refresh DAG** runs at 13:00, after the weather and air-quality DAGs have fetched the previous day's data at 12:00. It computes and inserts aggregates for the previous 24-hour window.

The daily refresh uses the raw data available for its date window. The full-refresh DAG recalculates the aggregates from the complete available raw history. Both produce rows only for hours with matching weather, traffic, and Atmo data.

## Daily Incremental Refresh Policy

The daily weather and air-quality ETL DAGs are scheduled at 12:00 and the aggregate DAG at 13:00. These are independent schedules: the aggregate DAG does not wait for or check the success of the source DAGs, and it does not validate source coverage or calculated rows before insertion.

The query starts from weather hours and joins traffic by hour and the Atmo daily aggregate by calendar date. An hour is omitted if it has no weather record, no matching traffic record for that traffic type, or no Atmo record for that date. Source coverage and calculated rows are not proactively checked.

The daily DAG uses `ON CONFLICT DO NOTHING`; rerunning it does not update rows already inserted for the same hour and traffic type. The full-refresh DAG deletes existing aggregate rows and inserts the rows returned by the query; it does not perform a separate completeness or result-validation step.

## Refresh Assumptions

The daily incremental refresh is correct under these assumptions:

- Source records for periods older than the refreshed 24-hour window are not modified after they have been processed.
- The aggregation logic and source schema have not changed since the previous refresh.
- All source loads covering the refreshed period have completed successfully before the aggregate DAG runs. This ordering is an operational assumption, not enforced by DAG dependencies.

If historical source data or aggregation logic changes, run the manual full-refresh DAG to recalculate the aggregate table from the complete raw history.

## Querying Strategy

FastAPI endpoints query the hourly aggregate dataset using the requested date range, traffic type, weekday, environmental metric, and optional pollutant subtype.

Indexes should support the main filter path, especially the hourly timestamp and traffic type. Additional indexes should only be added after examining real endpoint query plans with `EXPLAIN ANALYZE`.

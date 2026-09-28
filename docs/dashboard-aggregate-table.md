# Dashboard Aggregate Tables

## Purpose

The dashboard requires fast access to historical congestion and environmental data. To avoid repeatedly aggregating raw time-series tables for every API request, the database will store precomputed hourly aggregates for the measurements displayed by the dashboard.

These aggregate tables are intended for read-only historical analysis. FastAPI endpoints will query the precomputed data and apply dashboard filters, rather than recomputing the underlying averages from the raw tables.

## Aggregate Granularity

Each aggregate record represents one completed one-hour period. The aggregation key must include:

- The start timestamp of the hour.
- The traffic type, where the value is derived from tram ("ligne") or road-traffic data ("trr").

The hourly timestamp is the common join key for congestion, weather, and air-quality values. The dashboard aggregate table definitions are documented in `schema.md`.

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

The aggregate tables are refreshed through two separate Airflow DAGs:

- A **manual full-refresh DAG** rebuilds the complete hourly aggregate from all available raw source data. It is intended for initial population, source corrections, backfills, and changes to the aggregation logic.
- A **daily incremental-refresh DAG** runs at 13:00, after the weather and air-quality DAGs have fetched the previous day's data at 12:00. It rebuilds only the previous 24-hour window and updates the corresponding hourly records.

The daily refresh must be idempotent: rerunning it for the same date window must produce the same result from the same source data. The full-refresh DAG remains available to reflect corrections or backfills outside the daily window.

## Daily Incremental Refresh Policy

The weather and air-quality ETL DAGs fetch the previous day's data every day at 12:00. The daily aggregate DAG runs at 13:00, after these loads and after the traffic-source loads covering the same period have completed successfully.

The daily refresh workflow must:

1. Validate that the required congestion, weather, and pollution source data is available for the previous 24-hour window (and fail otherwise).
2. Rebuild the hourly aggregates for that window from the raw source tables, aggregating each source before joining them.
3. Validate the resulting hourly aggregates.
4. Replace the affected hourly records with the rebuilt records.

The incremental refresh should replace the affected time window rather than append blindly, so source corrections within that window are reflected and reruns remain idempotent.

The manual full refresh validates the complete rebuilt result, then replaces the contents of the aggregate table with the newly computed history.

## Refresh Assumptions

The daily incremental refresh is correct under these assumptions:

- Source records for periods older than the refreshed 24-hour window are not modified after they have been processed.
- The aggregation logic and source schema have not changed since the previous refresh.
- All source loads covering the refreshed period have completed successfully before the aggregate DAG runs.

If historical source data outside the 24-hour window is corrected, backfilled, deleted, or reprocessed, the incremental refresh is not sufficient. The manual full-refresh DAG must be run to rebuild the aggregate table from the complete raw history.

## Querying Strategy

FastAPI endpoints query the hourly aggregate dataset using the requested date range, traffic type, weekday, environmental metric, and optional pollutant subtype.

Indexes should support the main filter path, especially the hourly timestamp and traffic type. Additional indexes should only be added after examining real endpoint query plans with `EXPLAIN ANALYZE`.

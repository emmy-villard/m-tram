# Dashboard Materialized Hourly Aggregates

## Purpose

The dashboard requires fast access to historical congestion and environmental data. To avoid repeatedly aggregating raw time-series tables for every API request, the database will store materialized hourly averages for the measurements displayed by the dashboard.

These aggregates are intended for read-only historical analysis. FastAPI endpoints will query the materialized data and apply dashboard filters, rather than recomputing the underlying averages from the raw tables.

## Materialization Granularity

Each materialized record represents one completed one-hour period. The aggregation key must include:

- The start timestamp of the hour.
- The traffic type, where the value is derived from tram ("ligne") or road-traffic data ("trr").

The hourly timestamp is the common join key for congestion, weather, and air-quality values. The dashboard aggregate table definitions are documented in `schema.md`.

## Two-Hour Aggregates

The daily refresh also materializes two-hour aggregates from the freshly rebuilt hourly materialized table. This second layer avoids recalculating joins against the raw source tables while making predefined dashboard time blocks fast to query.

The two-hour table uses the selected block and the traffic type as aggregation dimensions. The DAG rebuilds it immediately after the hourly table has been fully materialized.

## Materialized Measurements

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

## Full Daily Rematerialization

The hourly materialized table is fully rebuilt every day. Historical records are not assumed to be immutable: each refresh recalculates all hourly aggregates from the current raw source data.

This policy ensures that source corrections, backfills, and transformation changes are reflected in the dashboard without requiring a separate maintenance operation.

## Daily Refresh Policy

The weather and air-quality ETL DAGs fetch the previous day's data every day at 12:00. The aggregate refresh must run only after these loads, and after the traffic-source loads for the same day have completed successfully.

The refresh workflow must:

1. Validate that the required congestion, weather, and pollution source data is available.
2. Rebuild the complete hourly materialized table from the raw source tables.
3. Validate the resulting hourly aggregates before making the refreshed table available to the API.
4. Rebuild the two-hour aggregate table from the freshly refreshed hourly table.

The rebuild should be atomic: the API must continue reading the previous valid table until the complete refreshed version is ready. Rerunning the workflow must safely produce the same result from the same source data.

## Querying Strategy

FastAPI endpoints query the materialized hourly dataset using the requested date range, traffic type, weekday, environmental metric, and optional pollutant subtype. Two-hour requests query the dedicated two-hour aggregate table.

Indexes should support the main filter path, especially the hourly timestamp and traffic type. Additional indexes should only be added after examining real endpoint query plans with `EXPLAIN ANALYZE`.

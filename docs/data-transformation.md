# Data Transformation - Explanatory Document
This document explains the cleansing and transformation rules applied across the ETL pipeline. For each data source, it covers:
1. the upstream source
2. the extraction and shape of the raw payload
3. the transformation steps applied before loading
4. the business rationale behind the rule
5. the assumptions made
6. the validation and expected impact

## Dynamic MData (trr, ligne)
1. The source is [MData](https://data.mobilites-m.fr/), which exposes live traffic data for the Grenoble area via endpoints such as `https://data.mobilites-m.fr/api/dyn/{type}/json`.
2. Each payload contains a dictionary keyed by a location identifier, with values including a timestamp and a traffic level (`nsv_id`). The project keeps only the fields needed for historical analysis: the entity identifier, the observation time, and the traffic level.
3. Rows whose `nsv_id` equals `0` are excluded because they indicate that no usable information is available for that reading. The valid range is `1` to `4`, where `1` is fluid traffic and `4` is a fully blocked or closed situation.
4. The assumptions are that the identifier is present, the timestamp is valid, and the traffic level is represented consistently across samples. This is enforced by the ETL validation layer before insertion.
5. The data is stored as a historical time series per road section or tram line. This enables analyses of congestion over time and makes the database the central archive for these indicators, which are not preserved elsewhere at this granularity.
6. The rule is validated in the transform tests under the ETL test suite and by the Pydantic schema checks before persistence.

## OpenMeteo
1. The source is the Open-Meteo API for the Grenoble location, accessed via a latitude/longitude endpoint configured in the ETL extract layer.
2. The raw response is a nested JSON payload under the `hourly` section. Each field is a list aligned by index, with timestamps in ISO format and meteorological measurements such as temperature, precipitation, pressure, wind, and weather code.
3. The transformation step converts the raw hourly dictionaries into a flat pandas DataFrame. `time` is parsed from ISO-8601 strings into a Python `datetime`, and each other value is kept as-is after validating its type and range.
4. The rationale is to normalize a complex API payload into a single tabular structure usable by SQLAlchemy and the database schema. This makes the dataset easier to validate, query, and compare with transport data.
5. The main assumption is that hourly fields remain aligned by index and that the payload is not empty. The validation schema checks duplicate timestamps and enforces realistic bounds (for example humidity in `[0, 100]`, cloud cover in `[0, 100]`, and non-negative precipitation values).
6. The expected impact is a clean daily/hourly weather history usable for correlation with traffic anomalies, travel conditions, and the effect of meteorological events on network performance.

## ATMO Auvergne-Rhône-Alpes
1. The source is the ATMO API, which exposes daily air-quality indices for the Grenoble area. The ETL fetch layer reads the API key from the environment and builds the endpoint using the configured commune identifier.
2. The raw response is a JSON object with a `success` flag and a list of `data` entries. Each entry contains a forecast or measured value, a date, and a set of pollutant sub-indices (`PM10`, `PM2.5`, `O3`, `NO2`, `SO2`).
3. The transformer iterates through each daily record, converts the date string to a timestamp, extracts the global pollution index, maps the measurement status (`réelle` vs `prévision`) to a boolean, and keeps the pollutant sub-indices in dedicated columns.
4. The rationale is to keep only the aggregated and domain-relevant indicators in a normalized table, while discarding structurally incomplete entries. This ensures the database stores stable pollutant metrics that can be joined with traffic and weather time series.
5. The assumptions are that the API response is successful, that the required keys and pollutant blocks exist for valid data, and that duplicate dates are not expected. Validation rejects empty data and duplicate primary keys on `time`.
6. The expected impact is a daily air-quality history that can be used to analyze whether pollution episodes correlate with changes in road or public-transport conditions.

## Shared ETL validation layer
All sources pass through a common pattern:
- extract a raw payload from an API,
- normalize it into a pandas DataFrame,
- validate the shape and value ranges with Pydantic schemas,
- load it into the relational model using SQLAlchemy.

This keeps the pipeline consistent across `trr`, `ligne`, `openmeteo`, and `atmo` and avoids persisting malformed or incomplete data.

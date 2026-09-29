# Sources
This document lists the data sources used by the ETL pipeline and the terms under which they are reused.

## Dynamic MData
These data come from [MData](https://data.mobilites-m.fr/donnees) and are freely available under the [ODbL licence](https://spdx.org/licenses/ODbL-1.0.html#licenseText).

### URLs
- `trr`: https://data.mobilites-m.fr/api/dyn/trr/json
- `ligne`: https://data.mobilites-m.fr/api/dyn/ligne/json

### Data description
The response is JSON-formatted. The JSON object is keyed by a unique identifier representing a road section or tram line. Each sample contains a timestamp and a traffic level (`nsv_id`):
- `0`: information unavailable
- `1`: fluid traffic
- `2`: slow traffic
- `3`: congestion / traffic jam
- `4`: closed

### Refresh frequency
The data is refreshed every few minutes and is not retained by the upstream provider unless it is harvested into the project database.

## Open-Meteo
This source provides meteorological time series for Grenoble and is used to enrich the traffic analysis with weather context.

### URL
The endpoint is built dynamically from the configured latitude/longitude coordinates, then requests the hourly weather variables exposed by Open-Meteo.

### Data description
The payload includes hourly observations and forecasts for multiple meteorological indicators, including:
- temperature and apparent temperature
- humidity
- precipitation and snowfall
- weather code
- pressure at sea level
- cloud cover
- wind speed and gusts

### Reuse conditions
Open-Meteo data is provided through its public API and is compatible with the project usage as a time-series source for retrospective analysis and dashboarding.

## ATMO Auvergne-Rhône-Alpes
This source provides air-quality indices for the Grenoble area and is used as a second environmental context alongside the weather feed.

### URL
The project reads the ATMO API endpoint using the commune-specific location and the environment variable `ATMO_API_KEY`.

### Data description
The returned JSON includes a global pollution score and pollutant sub-indices for the main atmospheric indicators such as PM10, PM2.5, O3, NO2, and SO2. A boolean field distinguishes measured values from forecast values.

### Pollution levels
The global pollution score and each pollutant sub-index range from `1` to `6`:

- `1`: good
- `2`: fair
- `3`: degraded
- `4`: poor
- `5`: very poor
- `6`: extremely poor

### Reuse conditions
ATMO data is retrieved through the public API and stored as a daily time series for analysis, with the project validating the response structure before inserting the rows into the database.
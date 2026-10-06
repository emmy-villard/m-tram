
# Congestion and Environmental Conditions Dashboard

## Purpose

This dashboard is an exploratory analytics tool for examining how public-transport or road-traffic congestion relates to weather conditions and air pollution. It enables users to compare congestion measurements for tram traffic or road traffic with pollution, rainfall, temperature, relative humidity, cloud cover, and wind data over a selected period.

The objective is to help identify patterns and potential correlations between congestion and environmental factors while keeping the analysis adjustable by date range, day of the week, and time of day.

## Main Visualization

The main view is a scatter plot that shows congestion in relation to one selected environmental metric. Visual series use the following color convention:

- Air pollution: brown
- Cumulative rainfall over the selected period: deep blue
- Average temperature: warm yellow
- Relative humidity: teal
- Cloud cover: deep gray
- Wind: light gray

Each plotted point represents the hourly aggregate for one timestamp that matches the active date-range and weekday filters. The time-of-day filter applies to hourly metrics and is disabled when air pollution is selected, because ATMO data is daily.

## Controls

### Dropdown Menus

- **Traffic type:** Select either tram congestion or road-traffic congestion.
- **Day of week:** Select all days or a specific day of the week.
- **Pollutant type:** When air pollution is selected, choose either the overall pollution indicator or one of the five available pollutant subtypes.

### Filters

- **Date range:** Last week, last month, last three months, last year, or all available data.
- **Time of day:** Disabled when air pollution is selected, because ATMO provides daily observations. The date-range and day-of-week filters remain available.
- **Time aggregation:** Display one point for each hourly observation in the selected dataset. Each point represents a specific `hour_start` timestamp; observations from the same hour of the day on different dates are not combined.

## Interaction

Selecting a point in the scatter plot opens a detail view containing the underlying fetched values for that observation. This allows users to inspect the congestion and environmental data represented by the point more precisely.

## Implementation

The dashboard is a single Streamlit page ([`src/streamlit_dashboard/main.py`](../src/streamlit_dashboard/main.py)). It has no database access: it fetches the hourly aggregates from the FastAPI route `GET /aggregate/{period}` and filters them in memory.

- **Configuration:** the API address is read from the `API_PROD_URL` environment variable (missing value raises an error). `https://` is prepended if no scheme is given.
- **Defaults:** road traffic, last month, temperature, all days, all hours.
- **Summary:** above the plot, the number of displayed points, the average congestion and the correlation between congestion and the selected metric.
- **Caching:** API responses are cached for 10 minutes per period.
- **Rainfall:** the plot shows the hourly rainfall, not the cumulative value over the period.
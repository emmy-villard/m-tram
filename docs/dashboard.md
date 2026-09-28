
# Congestion and Environmental Conditions Dashboard

## Purpose

This dashboard is an exploratory analytics tool for examining how tram and road traffic conditions relate to weather conditions and air pollution. It enables users to compare a selected traffic indicator with pollution, rainfall, temperature, relative humidity, cloud cover, and wind data over a selected period.

The traffic indicator can be tram-line congestion, road congestion, or the tram occupancy rate. Tram occupancy is planned but is not yet defined or available; see the TODO below.

The objective is to help identify patterns and potential correlations between congestion and environmental factors while keeping the analysis adjustable by date range, day of the week, and time of day.

## Main Visualization

The main view is a scatter plot that shows the selected traffic indicator in relation to one selected environmental metric. Visual series use the following color convention:

- Air pollution: brown
- Cumulative rainfall over the selected period: deep blue
- Average temperature: warm yellow
- Relative humidity: teal
- Cloud cover: deep gray
- Wind: light gray

Each plotted point represents an aggregated observation based on the active date, weekday, and time-grouping filters.

## Controls

### Dropdown Menus

- **Traffic indicator:** The planned choices are tram-line congestion, road congestion, and tram occupancy rate. Only the two congestion indicators are currently available; occupancy requires a definition and a data source first.
- **Day of week:** Select all days or a specific day of the week.
- **Pollutant type:** When air pollution is selected, choose either the overall pollution indicator or one of the five available pollutant subtypes.

### Filters

- **Date range:** Last week, last month, last three months, last year, or all available data.
- **Time aggregation:** Display observations aggregated by hour across the selected dataset. Each point corresponds to one hourly observation, irrespective of the specific date.

## Interaction

Selecting a point in the scatter plot opens a detail view containing the underlying fetched values for that observation. This allows users to inspect the selected traffic indicator and environmental data represented by the point more precisely.

## TODO

- Define the tram occupancy rate, identify its source data, and integrate its aggregation before making it selectable in the dashboard.
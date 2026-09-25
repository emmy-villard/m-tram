
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

Each plotted point represents an aggregated observation based on the active date, weekday, and time-grouping filters.

## Controls

### Dropdown Menus

- **Traffic type:** Select either tram congestion or road-traffic congestion.
- **Day of week:** Select all days or a specific day of the week.
- **Pollutant type:** When air pollution is selected, choose either the overall pollution indicator or one of the five available pollutant subtypes.
- **Two-hour time block:** When two-hour blocks are enabled, select one of the predefined periods:
    - Early morning: 04:30-06:30
    - Morning peak: 07:00-09:00
    - Midday: 11:00-13:00
    - Evening peak: 17:00-19:00
    - Late evening: 22:00-00:00

### Filters

- **Date range:** Last week, last month, last three months, last year, or all available data.
- **Time aggregation:** Choose between hourly averages and predefined two-hour blocks.
    - **Hourly averages:** Display observations aggregated by hour across the selected dataset. Each point corresponds to one hourly observation, irrespective of the specific date.
    - **Two-hour blocks:** Display observations aggregated for the selected two-hour block on each individual day. Selecting this mode reveals the two-hour time-block menu.

## Interaction

Selecting a point in the scatter plot opens a detail view containing the underlying fetched values for that observation. This allows users to inspect the congestion and environmental data represented by the point more precisely.
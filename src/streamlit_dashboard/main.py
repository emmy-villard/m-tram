import streamlit as st

st.set_page_config(
    page_title="M-Tram | Grenoble's congestion",
    page_icon="🚋",
    layout="wide",
)
st.title("M-Tram : Visualize Grenoble's congestion data")

import altair as alt
import pandas as pd
import requests

from util.env import get_env_var

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
PERIODS = {
    "Last week": "last_week",
    "Last month": "last_month",
    "Last 3 months": "last_three_months",
    "Last year": "last_year",
    "All data": "all_time",
}
TRAFFIC = {"Tram": "tram", "Road": "road"}
POLLUTANTS = {
    "Overall": "pollution_index",
    "PM10": "pm10_index",
    "PM2.5": "pm2_5_index",
    "O3": "o3_index",
    "NO2": "no2_index",
    "SO2": "so2_index",
}
# label -> (column, color)
METRICS = {
    "Air pollution": (None, "#8B5A2B"),
    "Rainfall": ("rainfall_total", "#1F3A93"),
    "Temperature": ("average_temperature", "#E5B300"),
    "Humidity": ("average_relative_humidity", "#008080"),
    "Cloud cover": ("average_cloud_cover", "#4A4A4A"),
    "Wind": ("average_wind_speed", "#B0B0B0"),
}


@st.cache_data(ttl=600)
def load_data(period: str) -> pd.DataFrame:
    base_url = get_env_var("API_PROD_URL").rstrip("/")
    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"
    response = requests.get(f"{base_url}/aggregate/{period}", timeout=60)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    if not df.empty:
        df["hour_start"] = pd.to_datetime(df["hour_start"])
    return df


# Controls
col1, col2, col3 = st.columns(3)
traffic = col1.segmented_control("Traffic type", list(TRAFFIC), default="Road")
period = col2.segmented_control("Period", list(PERIODS), default="Last month")
day = col3.selectbox("Day of week", ["All days"] + DAYS)

metric = st.segmented_control("Compare congestion with", list(METRICS), default="Temperature")

col4, col5 = st.columns(2)
pollutant = None
if metric == "Air pollution":
    pollutant = col4.selectbox("Pollutant", list(POLLUTANTS))
hours = col5.slider(
    "Time of day",
    0, 23, (0, 23),
    disabled=metric == "Air pollution",
    help="Disabled for air pollution: ATMO data is daily.",
)

if not (traffic and period and metric):
    st.info("Select a traffic type, a period and a metric.")
    st.stop()

# Data
try:
    df = load_data(PERIODS[period])
except Exception as e:
    st.error(f"Could not load data from the API: {e}")
    st.stop()

if df.empty:
    st.warning("No data available yet from the API.")
    st.stop()

df = df[df["traffic_type"] == TRAFFIC[traffic]]
if day != "All days":
    df = df[df["hour_start"].dt.dayofweek == DAYS.index(day)]
if metric != "Air pollution":
    df = df[df["hour_start"].dt.hour.between(*hours)]

column, color = METRICS[metric]
column = column or POLLUTANTS[pollutant]
df = df.dropna(subset=["average_congestion_level", column])
if df.empty:
    st.warning("No data for these filters.")
    st.stop()

# Summary
m1, m2, m3 = st.columns(3)
m1.metric("Points", len(df))
m2.metric("Average congestion", f"{df['average_congestion_level'].mean():.2f}")
m3.metric("Correlation", f"{df['average_congestion_level'].corr(df[column]):.2f}")

# Scatterplot
point = alt.selection_point(name="point", fields=["hour_start"], on="click")
chart = (
    alt.Chart(df)
    .mark_circle(size=60, color=color, opacity=0.7)
    .encode(
        x=alt.X(f"{column}:Q", title=pollutant or metric, scale=alt.Scale(zero=False)),
        y=alt.Y("average_congestion_level:Q", title=f"{traffic} congestion", scale=alt.Scale(domainMin=1)),
        tooltip=["hour_start", "average_congestion_level", column],
    )
    .add_params(point)
    .properties(height=500)
)
event = st.altair_chart(chart, width="stretch", on_select="rerun")

# Detail of the selected point
selected = event.selection.get("point", [])
if selected:
    ts = pd.to_datetime(selected[0]["hour_start"], unit="ms")
    st.subheader(f"Details: {ts}")
    st.dataframe(df[df["hour_start"] == ts].T, width="stretch")
else:
    st.caption("Click a point to see its details.")

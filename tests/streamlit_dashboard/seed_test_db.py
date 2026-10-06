"""
Fill the test database with fake hourly aggregates so the dashboard displays something.

The data is generated into aggregate_test_data.csv (dates end yesterday, so the
API date filters match), then loaded into dashboard_hourly_aggregates.
Usage: python tests/streamlit_dashboard/seed_test_db.py  (needs .env.test variables exported)
"""
import math
import os
import random
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import text

from db_connection.engine import engine

CSV_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "aggregate_test_data.csv")
DAYS = 60


def clip(value, low, high):
    return max(low, min(high, value))


def congestion_profile(hour, weekday):
    """Rush-hour shape in [0, 1]: two peaks on weekdays, a flat afternoon bump on weekends."""
    if weekday < 5:
        return math.exp(-((hour - 8) ** 2) / 3) + 0.9 * math.exp(-((hour - 17.5) ** 2) / 4) \
            + 0.25 * math.exp(-((hour - 12.5) ** 2) / 4)
    return 0.3 * math.exp(-((hour - 14) ** 2) / 18)


def generate_csv():
    """
    Synthetic data with the scales of the real aggregates: congestion is an
    average nsv_id in [1, 4], ATMO indices are daily integers in [1, 6],
    cloud cover and humidity are integer percentages. Congestion is
    deliberately independent of the weather and the pollution, as in the real data.
    """
    random.seed(42)
    last_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    first_day = last_day - timedelta(days=DAYS - 1)
    rows = []
    anomaly, cloudiness, pollution_state = 0.0, 0.5, 0.0
    for day_index in range(DAYS):
        day = first_day + timedelta(days=day_index)
        day_of_year = day.timetuple().tm_yday
        seasonal_temperature = 12 + 10.5 * math.cos(2 * math.pi * (day_of_year - 200) / 365)

        # Weather persists from one day to the next
        anomaly = 0.7 * anomaly + random.gauss(0, 2.5)
        cloudiness = clip(0.6 * cloudiness + random.betavariate(2, 2) * 0.4 + random.gauss(0, 0.1), 0, 1)
        rain_hours = set()
        intensity = 0.0
        if random.random() < 0.55 * cloudiness ** 2:
            start = random.randint(0, 20)
            rain_hours = set(range(start, min(24, start + random.randint(2, 10))))
            intensity = random.expovariate(1 / 0.8)
        daily_temperature = seasonal_temperature + anomaly - (2 if rain_hours else 0)

        # ATMO indices: one integer per day and pollutant, overall index is the worst one
        pollution_state = 0.75 * pollution_state + random.gauss(0, 0.8)
        pm10 = clip(round(1.6 + 0.6 * pollution_state + random.gauss(0, 0.4)), 1, 6)
        pm2_5 = clip(round(1.6 + 0.6 * pollution_state + random.gauss(0, 0.4)), 1, 6)
        o3 = clip(round(2 + 0.12 * (daily_temperature - 18) + 0.3 * pollution_state + random.gauss(0, 0.4)), 1, 6)
        no2 = clip(round(1.7 + 0.5 * pollution_state + random.gauss(0, 0.4)), 1, 6)
        so2 = 2 if random.random() < 0.05 else 1
        overall = max(pm10, pm2_5, o3, no2, so2)

        for hour in range(24):
            hour_start = day + timedelta(hours=hour)
            raining = hour in rain_hours
            diurnal_amplitude = 3 + 5 * (1 - cloudiness)
            temperature = daily_temperature + diurnal_amplitude * math.sin((hour - 9) / 24 * 2 * math.pi) \
                + random.gauss(0, 0.5)
            cloud_cover = 90 + random.randint(0, 10) if raining else clip(round(cloudiness * 100 + random.gauss(0, 15)), 0, 100)
            humidity = clip(round(85 - 1.6 * (temperature - 10) + (12 if raining else 0) + random.gauss(0, 5)), 25, 100)
            wind = random.gammavariate(2, 3) * (1 + 0.4 * math.sin((hour - 9) / 24 * 2 * math.pi)) + (3 if raining else 0)
            rain = round(max(0.0, random.gauss(intensity, intensity / 3)), 1) if raining else 0.0

            rush = congestion_profile(hour, hour_start.weekday())
            levels = {
                "road": 1.12 + 0.5 * rush + random.gauss(0, 0.04),
                "tram": 1.02 + 0.2 * rush + random.gauss(0, 0.03),
            }
            for traffic_type, level in levels.items():
                rows.append({
                    "hour_start": hour_start,
                    "traffic_type": traffic_type,
                    "average_congestion_level": round(clip(level, 1, 4), 3),
                    "pollution_index": float(overall),
                    "pm10_index": float(pm10),
                    "pm2_5_index": float(pm2_5),
                    "o3_index": float(o3),
                    "no2_index": float(no2),
                    "so2_index": float(so2),
                    "precipitation_total": rain,
                    "rainfall_total": rain,
                    "average_temperature": round(temperature, 1),
                    "average_relative_humidity": float(humidity),
                    "average_cloud_cover": float(cloud_cover),
                    "average_wind_speed": round(min(wind, 40), 1),
                })
    pd.DataFrame(rows).to_csv(CSV_PATH, index=False)


def load_csv():
    df = pd.read_csv(CSV_PATH, parse_dates=["hour_start"])
    with engine.begin() as connection:
        connection.execute(text("DELETE FROM dashboard_hourly_aggregates"))
        df.to_sql("dashboard_hourly_aggregates", connection, if_exists="append", index=False)
    print(f"Inserted {len(df)} rows into dashboard_hourly_aggregates")


if __name__ == "__main__":
    generate_csv()
    load_csv()

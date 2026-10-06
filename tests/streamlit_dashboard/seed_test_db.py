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


def generate_csv():
    random.seed(42)
    last_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    first_hour = last_day - timedelta(days=DAYS - 1)
    rows = []
    daily_pollution = {}
    for i in range(DAYS * 24):
        hour_start = first_hour + timedelta(hours=i)
        day = hour_start.date()
        if day not in daily_pollution:
            daily_pollution[day] = [random.uniform(1, 6) for _ in range(6)]
        temperature = 10 + 8 * math.sin((hour_start.hour - 9) / 24 * 2 * math.pi) + random.gauss(0, 2)
        rainfall = max(0, random.gauss(-0.5, 1))
        # Rush hours are more congested, rain makes it worse
        rush = math.exp(-((hour_start.hour - 8) ** 2) / 4) + math.exp(-((hour_start.hour - 17) ** 2) / 4)
        for traffic_type in ("tram", "road"):
            congestion = 0.2 + 0.4 * rush + 0.05 * rainfall + random.gauss(0, 0.05)
            pollution = daily_pollution[day]
            rows.append({
                "hour_start": hour_start,
                "traffic_type": traffic_type,
                "average_congestion_level": round(min(max(congestion, 0), 1), 3),
                "pollution_index": round(pollution[0], 2),
                "pm10_index": round(pollution[1], 2),
                "pm2_5_index": round(pollution[2], 2),
                "o3_index": round(pollution[3], 2),
                "no2_index": round(pollution[4], 2),
                "so2_index": round(pollution[5], 2),
                "precipitation_total": round(rainfall, 2),
                "rainfall_total": round(rainfall, 2),
                "average_temperature": round(temperature, 1),
                "average_relative_humidity": round(random.uniform(40, 95), 1),
                "average_cloud_cover": round(random.uniform(0, 100), 1),
                "average_wind_speed": round(random.uniform(0, 30), 1),
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

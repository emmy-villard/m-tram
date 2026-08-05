from sqlalchemy import URL, create_engine
import os

url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv('POSTGRES_USER'),
    host="localhost",
    port=os.getenv('POSTGRES_PORT'),
    database=os.getenv('POSTGRES_DB'),
    password=os.getenv('POSTGRES_PASSWORD'),
)
engine = create_engine(url)
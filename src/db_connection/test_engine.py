from sqlalchemy import URL, create_engine
from db_connection.util import get_env_var

"""
SQLAlchemy test url
"""

url = URL.create(
    drivername="postgresql+psycopg2",
    username=get_env_var('POSTGRES_TEST_USER'),
    host="localhost",
    port=get_env_var('POSTGRES_TEST_PORT'),
    database=get_env_var('POSTGRES_TEST_DB'),
    password=get_env_var('POSTGRES_TEST_PASSWORD'),
)

"""
SQLAlchemy test engine
"""
engine = create_engine(url)

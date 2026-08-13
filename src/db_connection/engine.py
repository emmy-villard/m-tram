from sqlalchemy import URL, create_engine
from db_connection.util import get_env_var

"""
SQLAlchemy database url
"""
url = URL.create(
    drivername="postgresql+psycopg2",
    username=get_env_var('POSTGRES_USER'),
    host="localhost",
    port=get_env_var('POSTGRES_PORT'),
    database=get_env_var('POSTGRES_DB'),
    password=get_env_var('POSTGRES_PASSWORD'),
)

"""
SQLAlchemy database engine
"""
engine = create_engine(url)

test_url = URL.create(
    drivername="postgresql+psycopg2",
    username=get_env_var('POSTGRES_TEST_USER'),
    host="localhost",
    port=get_env_var('POSTGRES_TEST_PORT'),
    database=get_env_var('POSTGRES_TEST_DB'),
    password=get_env_var('POSTGRES_TEST_PASSWORD'),
)

test_engine = create_engine(test_url)

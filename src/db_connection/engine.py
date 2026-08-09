from sqlalchemy import URL, create_engine
import os

"""
File for the engine Singleton
"""

def _get_env_var(name):
    var=os.getenv(name)
    if not var:
        raise ValueError(f"Environement variable {name} is empty")
    return var

"""
SQLAlchemy database url
"""
url = URL.create(
    drivername="postgresql+psycopg2",
    username=_get_env_var('POSTGRES_USER'),
    host="localhost",
    port=_get_env_var('POSTGRES_PORT'),
    database=_get_env_var('POSTGRES_DB'),
    password=_get_env_var('POSTGRES_PASSWORD'),
)

"""
SQLAlchemy database engine
"""
engine = create_engine(url)

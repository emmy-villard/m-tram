from sqlalchemy import URL, create_engine
import os

def _get_env_var(name):
    var=os.getenv(name)
    if not var:
        raise ValueError(f"Environement variable {name} is empty")
    return var

url = URL.create(
    drivername="postgresql+psycopg2",
    username=_get_env_var('POSTGRES_USER'),
    host="localhost",
    port=_get_env_var('POSTGRES_PORT'),
    database=_get_env_var('POSTGRES_DB'),
    password=_get_env_var('POSTGRES_PASSWORD'),
)
engine = create_engine(url)

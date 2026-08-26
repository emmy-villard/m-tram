from db_connection.test_engine import url, engine, get_env_var
from sqlalchemy import Engine


def test_engine_type():
    assert type(engine) == Engine

def test_URL_values():
    assert url.drivername == "postgresql+psycopg2"
    assert url.host == "localhost"
    assert url.username == get_env_var('POSTGRES_TEST_USER')
    assert url.port == int(get_env_var('POSTGRES_TEST_PORT'))
    assert url.database == get_env_var('POSTGRES_TEST_DB')
    assert url.password == get_env_var('POSTGRES_TEST_PASSWORD')
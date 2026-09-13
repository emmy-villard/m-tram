from db_connection.test_engine import url, engine, get_env_var
from sqlalchemy import Engine


def test_engine_type():
    assert type(engine) == Engine

def test_URL_values():
    assert url == get_env_var("TEST_DATABASE__SQL_ALCHEMY_CONN")
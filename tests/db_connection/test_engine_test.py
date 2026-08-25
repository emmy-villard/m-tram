from unittest.mock import patch
from db_connection.test_engine import url, engine
from sqlalchemy import Engine
import os


def test_engine_type():
    assert type(engine) == Engine

def test_URL_values():
    assert url.drivername == "postgresql+psycopg2"
    assert url.host == "localhost"
    assert url.username == os.getenv('POSTGRES_TEST_USER')
    assert url.port == int(os.getenv('POSTGRES_TEST_PORT'))
    assert url.database == os.getenv('POSTGRES_TEST_DB')
    assert url.password == os.getenv('POSTGRES_TEST_PASSWORD')
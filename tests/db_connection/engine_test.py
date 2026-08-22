from unittest.mock import patch
from db_connection.engine import url, engine
from sqlalchemy import Engine
import os


def test_engine_type():
    assert type(engine) == Engine

def test_URL_values():
    assert url == os.getenv('DATABASE__SQL_ALCHEMY_CONN')

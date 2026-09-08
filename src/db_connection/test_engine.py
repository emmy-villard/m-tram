from sqlalchemy import create_engine
from util.env import get_env_var

"""
SQLAlchemy test url
"""
url = get_env_var("TEST_DATABASE__SQL_ALCHEMY_CONN")

"""
SQLAlchemy test engine
"""
engine = create_engine(url)

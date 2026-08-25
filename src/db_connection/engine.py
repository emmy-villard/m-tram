from sqlalchemy import create_engine
from db_connection.util import get_env_var

"""
SQLAlchemy database url
"""
url = get_env_var("DATABASE__SQL_ALCHEMY_CONN")

"""
SQLAlchemy database engine
"""
engine = create_engine(url)
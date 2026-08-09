from orm.base import Base
from orm import ligne, trr
from db_connection.engine import engine

"""
Create database tables and relations
"""
Base.metadata.create_all(engine)
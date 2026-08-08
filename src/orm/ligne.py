from sqlalchemy import Column, Text, TIMESTAMP, Integer, PrimaryKeyConstraint
from orm.base import Base

class Ligne(Base):
    __tablename__ = "ligne"

    ligne_id = Column(Text)
    ligne_time = Column(TIMESTAMP)
    ligne_nsv_id = Column(Integer)
    pk = PrimaryKeyConstraint(ligne_id, ligne_time)

    def __repr__(self) -> str:
        return f"ligne(ligne_id={self.ligne_id}, ligne_time={self.ligne_time}, ligne_nsv_id={self.ligne__nsv_id})"

class NewLigneData(Base):
    __tablename__ = "new_ligne_data"

    ligne_id = Column(Text)
    ligne_time = Column(TIMESTAMP)
    ligne_nsv_id = Column(Integer)
    pk = PrimaryKeyConstraint(ligne_id, ligne_time)

    def __repr__(self) -> str:
        return f"new_ligne_data(ligne_id={self.ligne_id}, ligne_time={self.ligne_time}, ligne__nsv_id={self.ligne__nsv_id})"
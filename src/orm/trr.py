from sqlalchemy import Column, Text, TIMESTAMP, Integer, PrimaryKeyConstraint
from orm.base import Base

class Trr(Base):
    __tablename__ = "trr"

    trr_id = Column(Text)
    trr_time = Column(TIMESTAMP)
    trr_nsv_id = Column(Integer)
    pk = PrimaryKeyConstraint(trr_id, trr_time)

    def __repr__(self) -> str:
        return f"trr(trr_id={self.trr_id}, trr_time={self.trr_time}, trr_nsv_id={self.trr_nsv_id})"

class NewTrrData(Base):
    __tablename__ = "new_trr_data"

    trr_id = Column(Text)
    trr_time = Column(TIMESTAMP)
    trr_nsv_id = Column(Integer)
    pk = PrimaryKeyConstraint(trr_id, trr_time)

    def __repr__(self) -> str:
        return f"new_trr_data(trr_id={self.trr_id}, trr_time={self.trr_time}, trr__nsv_id={self.trr_nsv_id})"
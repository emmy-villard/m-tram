from sqlalchemy import Text, TIMESTAMP, Integer
from sqlalchemy.orm import Mapped, mapped_column
from orm.base import Base
from datetime import datetime


class Trr(Base):
    """
    Class definition of table : "trr". Used to store long-term "ligne" data about traffic conditions in Grenoble

    Properties
    ----------
    
    trr_id : sqlalchemy.Column(sqlalchemy.Text)
        section of road id
    trr_id : sqlalchemy.Column(sqlalchemy.TIMESTAMP)
        report timestamp
    trr_nsv_id : sqlalchemy.Column(sqlalchemy.Integer)
        traffic condition
    """
    __tablename__ = "trr"

    trr_id: Mapped[str] = mapped_column(Text, primary_key=True)
    trr_time: Mapped[datetime] = mapped_column(TIMESTAMP, primary_key=True)
    trr_nsv_id: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"trr(trr_id={self.trr_id}, trr_time={self.trr_time}, trr_nsv_id={self.trr_nsv_id})"

class NewTrrData(Base):
    """
    Class definition of table : "new_trr_data". Used for temporary storage

    Properties
    ----------
    
    trr_id : sqlalchemy.Column(sqlalchemy.Text)
        section of road id
    trr_id : sqlalchemy.Column(sqlalchemy.TIMESTAMP)
        report timestamp
    trr_nsv_id : sqlalchemy.Column(sqlalchemy.Integer)
        traffic condition
    """
    __tablename__ = "new_trr_data"

    trr_id: Mapped[str] = mapped_column(Text, primary_key=True)
    trr_time: Mapped[datetime] = mapped_column(TIMESTAMP, primary_key=True)
    trr_nsv_id: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"new_trr_data(trr_id={self.trr_id}, trr_time={self.trr_time}, trr__nsv_id={self.trr_nsv_id})"
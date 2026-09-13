from sqlalchemy import Text, TIMESTAMP, Integer
from sqlalchemy.orm import Mapped, mapped_column
from orm.base import Base
from datetime import datetime

class Ligne(Base):
    """
    Class definition of table : "ligne". Used to store long-term "ligne" data about tram traffic conditions in Grenoble

    Properties
    ----------
    
    ligne_id : sqlalchemy.mapped_column(sqlalchemy.Text)
        tram line
    ligne_id : sqlalchemy.mapped_column(sqlalchemy.TIMESTAMP)
        report timestamp
    ligne_nsv_id : sqlalchemy.mapped_column(sqlalchemy.Integer)
        traffic condition
    """
    __tablename__ = "ligne"

    ligne_id: Mapped[str] = mapped_column(Text, primary_key=True)
    ligne_time: Mapped[datetime] = mapped_column(TIMESTAMP, primary_key=True)
    ligne_nsv_id: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"ligne(ligne_id={self.ligne_id}, ligne_time={self.ligne_time}, ligne_nsv_id={self.ligne_nsv_id})"
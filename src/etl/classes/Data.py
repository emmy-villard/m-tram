from abc import ABC, abstractmethod
import pandas as pd
from sqlalchemy import Engine
from orm.base import Base
from pydantic import BaseModel
from typing import Callable, Sequence

class Data(ABC):
    """
    Functions wrapper for each data source
    """
    @staticmethod
    @abstractmethod
    def get_url() -> str:
        pass

    @staticmethod
    @abstractmethod
    def fetch(url) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def raw_data_to_df(raw_data) -> pd.DataFrame:
        pass

    @staticmethod
    @abstractmethod
    def load_table(dataframe, engine, orm_class, data_validator):
        pass

    @staticmethod
    @abstractmethod
    def engine() -> Engine:
        pass

    @staticmethod
    @abstractmethod
    def orm_class() -> type[Base]:
        pass

    @staticmethod
    @abstractmethod
    def data_validator() -> Callable[[pd.DataFrame], Sequence[BaseModel]]:
        pass
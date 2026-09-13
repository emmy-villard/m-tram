from pydantic import BaseModel, TypeAdapter, Field
from datetime import datetime
from typing import List, Sequence, Literal
from pandas import DataFrame

class TrrSchema(BaseModel):
    trr_id: str
    trr_time: datetime
    trr_nsv_id: Literal[1, 2, 3, 4]

def validate_trr_data(dataframe: DataFrame) -> Sequence[BaseModel]:
    """
    validates trr data and returns the data
    """
    if dataframe.empty:
        raise ValueError("trr data cannot be empty")

    if dataframe.duplicated(subset=["trr_id", "trr_time"]).any():
        raise ValueError("duplicate primary key : " \
            "trr_id and trr_time must be unique together")

    records = dataframe.to_dict("records")
    return TypeAdapter(List[TrrSchema]).validate_python(records)
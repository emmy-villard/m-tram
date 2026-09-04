from pydantic import BaseModel, TypeAdapter, Field
from datetime import datetime
from typing import List
from pandas import DataFrame

class LigneSchema(BaseModel):
    ligne_id: str
    ligne_time: datetime
    ligne_nsv_id: int = Field(ge=1, le=4)

def convert_ligne_data(dataframe: DataFrame):
    if dataframe.empty:
        raise ValueError("ligne data cannot be empty")

    dataframe_with_id = dataframe.reset_index()
    if dataframe_with_id.duplicated(subset=["ligne_id", "ligne_time"]).any():
        raise ValueError("duplicate primary key : " \
            "ligne_id and ligne_time must be unique together")

    records = dataframe_with_id.to_dict("records")
    return TypeAdapter(List[LigneSchema]).validate_python(records)
from pydantic import BaseModel, TypeAdapter, Field
from datetime import datetime
from typing import List, Sequence, Literal
from pandas import DataFrame

class LigneSchema(BaseModel):
    ligne_id: str
    ligne_time: datetime
    ligne_nsv_id: Literal[1, 2, 3, 4]

def validate_ligne_data(dataframe: DataFrame) -> Sequence[BaseModel]:
    """
    validates ligne data and returns the data
    """
    if dataframe.empty:
        raise ValueError("ligne data cannot be empty")

    if dataframe.duplicated(subset=["ligne_id", "ligne_time"]).any():
        raise ValueError("duplicate primary key : " \
            "ligne_id and ligne_time must be unique together")

    records = dataframe.to_dict("records")
    return TypeAdapter(List[LigneSchema]).validate_python(records)
from pydantic import BaseModel, TypeAdapter
from datetime import datetime
from typing import List, Literal, Sequence
from pandas import DataFrame

class AtmoSchema(BaseModel):
    time: datetime
    pollution_index: Literal[1, 2, 3, 4, 5, 6]
    is_value_mesured: bool
    PM10_index: Literal[1, 2, 3, 4, 5, 6]
    PM2_5_index: Literal[1, 2, 3, 4, 5, 6]
    O3_index: Literal[1, 2, 3, 4, 5, 6]
    NO2_index: Literal[1, 2, 3, 4, 5, 6]
    SO2_index: Literal[1, 2, 3, 4, 5, 6]

def validate_atmo_data(dataframe: DataFrame) -> Sequence[BaseModel]:
    """
    validates atmo data and returns the data
    """
    if dataframe.empty:
        raise ValueError("openmeteo data cannot be empty")
    
    dataframe_with_id = dataframe.reset_index()
    if dataframe_with_id.duplicated(subset=["time"]).any():
        raise ValueError("duplicate primary key : time must be unique")
    
    records = dataframe_with_id.to_dict("records")
    return TypeAdapter(List[AtmoSchema]).validate_python(records)
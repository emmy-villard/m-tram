from pydantic import BaseModel, TypeAdapter, Field
from datetime import datetime
from typing import List, Literal, Sequence
from pandas import DataFrame

class OpenMeteoSchema(BaseModel):
    time: datetime
    temperature_2m: float = Field(ge=-272)
    apparent_temperature: float = Field(ge=-272)
    relativehumidity_2m: int = Field(ge=0, le=100)
    precipitation: float = Field(ge=0)
    rain: float = Field(ge=0)
    snowfall: float = Field(ge=0)
    weathercode: Literal[
        0, 1, 2, 3, 45, 48, 51, 53, 55, 56, 57, 61, 63, 65,
        66, 67, 71, 73, 75, 77, 80, 81, 82, 85, 86, 95, 96, 99
    ]
    pressure_msl: float = Field(ge=0)
    cloudcover: int = Field(ge=0, le=100)
    windspeed_10m: float = Field(ge=0)
    windgusts_10m: float = Field(ge=0)

def validate_openmeteo_data(dataframe: DataFrame) -> Sequence[BaseModel]:
    """
    validates openmeteo data and returns the data
    """
    if dataframe.empty:
        raise ValueError("openmeteo data cannot be empty")
    
    dataframe_with_id = dataframe.reset_index()
    if dataframe_with_id.duplicated(subset=["time"]).any():
        raise ValueError("duplicate primary key : time must be unique")
    
    records = dataframe_with_id.to_dict("records")
    return TypeAdapter(List[OpenMeteoSchema]).validate_python(records)
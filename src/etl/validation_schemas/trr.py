from pydantic import BaseModel, TypeAdapter
from datetime import datetime
from typing import List
from pandas import DataFrame

class TrrSchema(BaseModel):
    trr_id: str
    trr_time: datetime
    trr_nsv_id: int

def check_trr_data(dataframe: DataFrame):
    data = dataframe.reset_index().to_dict('records')
    validator = TypeAdapter(List[TrrSchema])
    validator.validate_python(data)
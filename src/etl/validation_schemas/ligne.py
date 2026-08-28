from pydantic import BaseModel, TypeAdapter
from datetime import datetime
from typing import List
from pandas import DataFrame

class LigneSchema(BaseModel):
    ligne_id: str
    ligne_time: datetime
    ligne_nsv_id: int

def check_ligne_data(dataframe: DataFrame):
    data = dataframe.reset_index().to_dict('records')
    validator = TypeAdapter(List[LigneSchema])
    validator.validate_python(data)
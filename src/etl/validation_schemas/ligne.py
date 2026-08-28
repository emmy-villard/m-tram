from pydantic import BaseModel, TypeAdapter, Field
from datetime import datetime
from typing import List
from pandas import DataFrame

class LigneSchema(BaseModel):
    ligne_id: str
    ligne_time: datetime
    ligne_nsv_id: int = Field(ge=1, le=4)

def check_ligne_data(dataframe: DataFrame):
    data = dataframe.reset_index().to_dict('records')
    validator = TypeAdapter(List[LigneSchema])
    validator.validate_python(data)
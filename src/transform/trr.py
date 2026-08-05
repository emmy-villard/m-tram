import pandas as pd
from datetime import datetime

def raw_to_pandas_trr(response_dict_ttr):
    data = [[
        k,
        datetime.fromtimestamp(value[0]["time"] / 1000),
        value[0]["nsv_id"]
    ] for k, value in response_dict_ttr.items()]

    dataframe_trr = pd.DataFrame(data,
        columns=("trr_id", "trr_time", "trr_nsv_id")
    ).set_index("trr_id")

    return dataframe_trr
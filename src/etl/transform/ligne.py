import pandas as pd
from datetime import datetime

def raw_to_pandas_ligne(response_dict):
    """
    Transforms raw "ligne" data into clean pandas DataFrame

    Parameters
    ----------
    response_dict : dictionary
        Raw json ligne data

    Returns
    -------
    pandas.DataFrame
        Transformed data
    """
    data = [[
        k,
        datetime.fromtimestamp(value["time"] / 1000),
        value["nsv_id"]
    ] for k, value in response_dict.items() if value["nsv_id"] != 0]

    dataframe = pd.DataFrame(data,
        columns=("ligne_id", "ligne_time", "ligne_nsv_id")
    ).set_index("ligne_id")

    return dataframe
import pandas as pd
from datetime import datetime
import logging

def raw_to_pandas_trr(response_dict):
    """
    Transforms raw "trr" data into clean pandas DataFrame

    Parameters
    ----------
    response_dict : dictionary
        Raw json trr data

    Returns
    -------
    pandas.DataFrame
        Transformed data
    """
    data = list()
    for k, value in response_dict.items():
        try:
            value = value[0]
            if value["nsv_id"] != 0:
                data.append([
                    k,
                    datetime.fromtimestamp(value["time"] / 1000),
                    value["nsv_id"]
                ])
        except(KeyError):
            logging.info("Dropped line %s", value)
            continue
    dataframe_trr = pd.DataFrame(data,
        columns=("trr_id", "trr_time", "trr_nsv_id")
    )

    return dataframe_trr
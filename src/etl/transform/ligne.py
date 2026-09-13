import pandas as pd
from datetime import datetime
import logging

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
    data = list()
    for k, value in response_dict.items():
        try:
            if value["nsv_id"] != 0:
                data.append([
                    k,
                    datetime.fromtimestamp(value["time"] / 1000),
                    value["nsv_id"]
                ])
        except(KeyError):
            logging.info("Dropped line %s", value)
            continue
    dataframe = pd.DataFrame(data,
        columns=("ligne_id", "ligne_time", "ligne_nsv_id")
    )

    return dataframe
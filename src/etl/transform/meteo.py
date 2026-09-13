import pandas as pd
from datetime import datetime
import logging

def raw_to_pandas_meteo(response_dict):
    """
    Transforms raw "openapi_meteo" data into clean pandas DataFrame

    Parameters
    ----------
    response_dict : dictionary
        Raw json openapi_meteo data

    Returns
    -------
    pandas.DataFrame
        Transformed data
    """
    if not response_dict:
        raise ValueError("empty openmeteo response")
    data = response_dict["hourly"]
    nhours = len(data["time"])
    useful_data = list()
    for hour in range(nhours):
        try:
            useful_data.append([
                process_meteo_data(key, data[key][hour]) for key in data.keys()
            ])
        except(KeyError, IndexError):
            logging.info("Dropped line %s", hour)
            continue
    dataframe = pd.DataFrame(
        useful_data,
        columns=data.keys()
    )
    return dataframe

def str_to_datetime(str):
    return datetime.strptime(str, "%Y-%m-%dT%H:%M")

def process_meteo_data(key, data):
    if (key=="time"):
        return str_to_datetime(data)
    return data
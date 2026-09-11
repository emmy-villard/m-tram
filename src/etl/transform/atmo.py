import pandas as pd
from datetime import datetime

def raw_to_pandas_atmo(response_dict):
    """
    Transforms raw "atmo" data into clean pandas DataFrame

    Parameters
    ----------
    response_dict : dictionary
        Raw json atmo data

    Returns
    -------
    pandas.DataFrame
        Transformed data
    """
    """
    data = [[
        k,
        datetime.fromtimestamp(value["time"] / 1000),
        value["nsv_id"]
    ] for k, value in response_dict.items() if value["nsv_id"] != 0]

    dataframe = pd.DataFrame(data,
        columns=("ligne_id", "ligne_time", "ligne_nsv_id")
    ).set_index("ligne_id")
    """
    if not response_dict:
        raise ValueError("empty openmeteo response")
    if not response_dict["success"]:
        raise ValueError("atmo api fetch failed")
    print(len(response_dict["data"]))
    data = [
        [
            _str_to_datetime(day_data["date_echeance"]),
            day_data["indice"],
            _is_value_mesured(day_data["type_valeur"]),
            day_data["sous_indices"][0]["indice"],
            day_data["sous_indices"][1]["indice"],
            day_data["sous_indices"][2]["indice"],
            day_data["sous_indices"][3]["indice"],
            day_data["sous_indices"][4]["indice"],

        ] for day_data in response_dict["data"]
    ]
    columns = ["time", "pollution_index", "is_value_mesured",
        "PM10_index", "PM2_5_index", "O3_index", "NO2_index", "SO2_index"
    ]
    dataframe = pd.DataFrame(data, columns=columns)
    return dataframe

def _is_value_mesured(value_type:str) -> int:
    if value_type=="réelle":
        return True
    if value_type=="prévision":
        return False
    raise ValueError(f"Unknown value type in atmo json: {type}")

def _str_to_datetime(str):
    return datetime.strptime(str, "%Y-%m-%d")
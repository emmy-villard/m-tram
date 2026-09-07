import os, json
from etl.transform.ligne import raw_to_pandas_ligne
from etl.transform.trr import raw_to_pandas_trr
from etl.transform.meteo import raw_to_pandas_meteo

dir_path = os.path.dirname(os.path.realpath(__file__))

def _get_data(file_path):
    with open(dir_path + f"/{file_path}.json") as file:
        return json.load(file)
    
if __name__ == "__main__":
    raw_data = _get_data("ligne")
    dataframe = raw_to_pandas_ligne(raw_data)
    dataframe.to_csv(dir_path + "/ligne.csv")

    raw_data = _get_data("trr")
    dataframe = raw_to_pandas_trr(raw_data)
    dataframe.to_csv(dir_path + "/trr.csv")

    raw_data = _get_data("openmeteo")
    dataframe = raw_to_pandas_meteo(raw_data)
    dataframe.to_csv(dir_path + "/openmeteo.csv")
import os, json
from etl.transform.ligne import raw_to_pandas_ligne
from etl.transform.trr import raw_to_pandas_trr

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(dir_path + "/ligne.json") as file:
        raw_data = json.load(file)
    dataframe = raw_to_pandas_ligne(raw_data)
    dataframe.to_csv(dir_path + "/ligne.csv")

    with open(dir_path + "/trr.json") as file:
        raw_data = json.load(file)
    dataframe = raw_to_pandas_trr(raw_data)
    dataframe.to_csv(dir_path + "/trr.csv")
    
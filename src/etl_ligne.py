from extract.ligne import fetch_ligne
from transform.ligne import raw_to_pandas_ligne
from load.ligne import load_ligne

def etl_ligne():
    raw_data = fetch_ligne()
    dataframe = raw_to_pandas_ligne(raw_data)
    load_ligne(dataframe)

if __name__ == "__main__":
    etl_ligne()
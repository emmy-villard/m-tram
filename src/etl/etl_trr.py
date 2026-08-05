from extract.trr import fetch_trr
from transform.trr import raw_to_pandas_trr
from load.mdata_dyn import load_table

def etl_trr():
    raw_data = fetch_trr()
    dataframe = raw_to_pandas_trr(raw_data)
    load_table(dataframe, "trr")

if __name__ == "__main__":
    etl_trr()
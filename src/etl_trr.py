from extract.trr import fetch_trr
from transform.trr import raw_to_pandas_trr
from load.trr import load_trr

raw_data = fetch_trr()
dataframe = raw_to_pandas_trr(raw_data)
load_trr(dataframe)
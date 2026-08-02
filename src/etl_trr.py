from extract.fetch_data_trr import fetch_trr
from transform.transform_trr import raw_to_pandas_trr

raw_data = fetch_trr()
dataframe = raw_to_pandas_trr(raw_data)
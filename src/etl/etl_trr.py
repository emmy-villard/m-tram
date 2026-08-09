from etl.extract.trr import fetch_trr
from etl.transform.trr import raw_to_pandas_trr
from etl.load.mdata_dyn import load_table
from orm.trr import Trr, NewTrrData

def etl_trr():
    """
    Launches ETL procedure for data "trr"

    Parameters
    ----------

    Returns
    -------
    """
    raw_data = fetch_trr()
    dataframe = raw_to_pandas_trr(raw_data)
    load_table(dataframe, Trr, NewTrrData)

if __name__ == "__main__":
    etl_trr()
from etl.extract.api_url import url_trr
from etl.extract.fetch_api import fetch_api
from etl.transform.trr import raw_to_pandas_trr
from etl.load.mdata_dyn import load_table
from orm.trr import Trr, NewTrrData
from db_connection.engine import engine

def etl_trr():
    """
    Launches ETL procedure for data "trr"

    Parameters
    ----------

    Returns
    -------
    """
    raw_data = fetch_api(url_trr)
    dataframe = raw_to_pandas_trr(raw_data)
    load_table(dataframe, engine, Trr, NewTrrData)

if __name__ == "__main__":
    etl_trr()
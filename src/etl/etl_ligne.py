from etl.extract.api_url import url_ligne
from etl.extract.fetch_api import fetch_api
from etl.transform.ligne import raw_to_pandas_ligne
from etl.load.mdata_dyn import load_table
from orm.ligne import Ligne, NewLigneData
from db_connection.engine import engine

def etl_ligne():
    """
    Launches ETL procedure for data "ligne"

    Parameters
    ----------

    Returns
    -------
    """
    raw_data = fetch_api(url_ligne)
    dataframe = raw_to_pandas_ligne(raw_data)
    load_table(dataframe, engine, Ligne, NewLigneData)

if __name__ == "__main__":
    etl_ligne()
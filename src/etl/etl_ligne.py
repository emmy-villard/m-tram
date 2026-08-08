from etl.extract.ligne import fetch_ligne
from etl.transform.ligne import raw_to_pandas_ligne
from etl.load.mdata_dyn import load_table
from orm.ligne import Ligne, NewLigneData

def etl_ligne():
    raw_data = fetch_ligne()
    dataframe = raw_to_pandas_ligne(raw_data)
    load_table(dataframe, Ligne, NewLigneData)

if __name__ == "__main__":
    etl_ligne()
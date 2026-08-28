from etl.validation_schemas.ligne import check_ligne_data
import os
import pandas as pd

def test_validate_static_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dataframe = pd.read_csv(dir_path + "/../etl_test_data/ligne.csv")
    check_ligne_data(dataframe)
from etl.load.mdata_dyn import load_table
from unittest.mock import patch, MagicMock
import sqlalchemy
import pandas as pd
from datetime import datetime
from orm.trr import Trr, NewTrrData

def test_load_table():
    with patch("etl.load.mdata_dyn.Session", new_callable=MagicMock) as mock_session, \
        patch("pandas.DataFrame.to_sql") as mock_sql:
            mock_sess = mock_session.return_value.__enter__.return_value
            load_table(pd.DataFrame([]), (), Trr, NewTrrData)
            mock_sess.execute.assert_called()
            mock_sess.commit.assert_called()
            mock_sql.assert_called()
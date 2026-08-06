from etl.load.mdata_dyn import load_table, getTables
from unittest.mock import patch, MagicMock
import sqlalchemy
import pandas as pd
from datetime import datetime

def test_column_types_Table():
    table, new_table_data = getTables("test")
    assert type(table) == sqlalchemy.Table
    assert type(new_table_data) == sqlalchemy.Table
    assert type(table.c.test_id.type) == sqlalchemy.Text
    assert type(table.c.test_time.type) == sqlalchemy.TIMESTAMP
    assert type(table.c.test_nsv_id.type) == sqlalchemy.Integer
    assert type(new_table_data.c.test_id.type) == sqlalchemy.Text
    assert type(new_table_data.c.test_time.type) == sqlalchemy.TIMESTAMP
    assert type(new_table_data.c.test_nsv_id.type) == sqlalchemy.Integer
    assert len(table.constraints) > 0
    assert len(new_table_data.constraints) > 0


def test_load_table():
    with patch("sqlalchemy.Engine.connect", new_callable=MagicMock) as mock_connect, \
        patch("pandas.DataFrame.to_sql") as mock_sql:
            mock_conn = mock_connect.return_value.__enter__.return_value
            load_table(pd.DataFrame([]), "trr")
            mock_conn.execute.assert_called()
            mock_conn.commit.assert_called()
            mock_sql.assert_called()

class Mock_connect(MagicMock):
    def execute(statement):
        pass
    def commit():
        pass
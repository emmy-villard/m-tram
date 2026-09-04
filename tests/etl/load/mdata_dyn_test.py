from etl.load.mdata_dyn import load_table
from unittest.mock import patch, MagicMock
import pandas as pd
from orm.trr import Trr
import pytest

@pytest.fixture
def mock_converter():
    return MagicMock()

def test_load_table(mock_converter):
    with patch("etl.load.mdata_dyn.Session", new_callable=MagicMock) as mock_session:
        mock_sess = mock_session.return_value.__enter__.return_value
        load_table(pd.DataFrame([]), (), Trr, mock_converter)
        mock_converter.assert_called()

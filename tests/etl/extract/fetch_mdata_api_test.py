from unittest.mock import patch
from etl.extract.api_url import url_ligne, url_trr
from etl.extract.fetch_mdata_api import fetch_mdata_api
import os, json
import pytest

@pytest.fixture
def returned_data_ligne():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/../etl_test_data/ligne.json") as file:
        return json.load(file)

@pytest.fixture
def returned_data_ttr():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/../etl_test_data/ttr.json") as file:
        return json.load(file)

@pytest.mark.parametrize("url", [(url_ligne), (url_trr)])
def test_requests_get_called(url):
    with patch("requests.get") as mock_get:
        fetch_mdata_api(url)
        mock_get.assert_called_with(url)

@pytest.mark.parametrize("returned_data, url", [
    (returned_data_ligne, url_ligne),
    (returned_data_ttr, url_trr)
])
def test_returned_value(returned_data, url):
    with patch("requests.Response") as mock_Response, \
    patch("requests.get", return_value=mock_Response) as mock_get, \
    patch("requests.Response.json", return_value = returned_data):
        assert returned_data == fetch_mdata_api(url)
        assert returned_data != {}
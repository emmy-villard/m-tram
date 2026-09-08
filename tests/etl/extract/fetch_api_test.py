from unittest.mock import patch
from etl.extract.endpoint_url.mdata_ligne import get_url as get_url_ligne
from etl.extract.endpoint_url.mdata_trr import get_url as get_url_trr
from etl.extract.endpoint_url.openmeteo import get_url as get_url_openapi_meteo
from etl.extract.fetch_api import fetch_api
import os, json
import pytest


def read_file(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + f"/../etl_test_data/{file_name}.json") as file:
        return json.load(file)

@pytest.fixture
def returned_data_ligne():
    return read_file("ligne")

@pytest.fixture
def returned_data_ttr():
    return read_file("trr")

@pytest.fixture
def retruned_data_openmeteo():
    return read_file("openmeteo")

@pytest.mark.parametrize("get_url", [
    (get_url_ligne),
    (get_url_trr),
    (get_url_openapi_meteo)
])
def test_requests_get_called(get_url):
    with patch("requests.get") as mock_get:
        url = get_url()
        fetch_api(url)
        mock_get.assert_called_with(url)

@pytest.mark.parametrize(["returned_data", "get_url"], [
    (returned_data_ligne, get_url_ligne),
    (returned_data_ttr, get_url_trr),
    (retruned_data_openmeteo, get_url_openapi_meteo)
])
def test_returned_value(returned_data, get_url):
    with patch("requests.Response") as mock_Response, \
    patch("requests.get", return_value=mock_Response) as mock_get, \
    patch("requests.Response.json", return_value = returned_data):
        url = get_url()
        assert returned_data == fetch_api(url)
        assert returned_data != {}
        mock_get.assert_called_with(url)
from unittest.mock import patch
from etl.extract.trr import fetch_trr
import os, json

url_trr = "https://data.mobilites-m.fr/api/dyn/trr/json"
returned_data = {}
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/../etl_test_data/trr.json") as file:
    returned_data = json.load(file)


def test_requests_get_called():
    with patch("requests.get") as mock_get:
        fetch_trr()
        mock_get.assert_called_with(url_trr)

def test_returned_value():
    with patch("requests.Response") as mock_Response, \
    patch("requests.get", return_value=mock_Response) as mock_get, \
    patch("requests.Response.json", return_value=returned_data):
        assert returned_data == fetch_trr()
        assert returned_data != {}
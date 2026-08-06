from unittest.mock import patch
from etl.extract.ligne import fetch_ligne
import os, json

url_ligne = "https://data.mobilites-m.fr/api/dyn/ligne/json"
returned_data = {}
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/../etl_test_data/ligne.json") as file:
    returned_data = json.load(file)


def test_requests_get_called():
    with patch("requests.get") as mock_get:
        fetch_ligne()
        mock_get.assert_called_with(url_ligne)

def test_returned_value():
    with patch("requests.Response") as mock_Response:
        with patch("requests.get", return_value=mock_Response) as mock_get:
            with patch("requests.Response.json", return_value = returned_data):
                assert returned_data == fetch_ligne()
                assert returned_data != {}
from etl.extract.endpoint_url.mdata_trr import get_url
import requests

def test_is_valid_endpoint():
    url = get_url()
    response = requests.get(url, timeout=30)
    response.raise_for_status()
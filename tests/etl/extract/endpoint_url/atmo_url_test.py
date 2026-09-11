from etl.extract.endpoint_url.atmo import get_url
from datetime import datetime, timedelta
import pytest
from urllib.parse import urlparse, parse_qsl
from util.date import date_format
import requests

def test_is_valid_endpoint():
    url = get_url()
    response = requests.get(url)
    assert response.status_code == 200

def get_param(start_date, get_range_of_days, key):
    url = get_url(start_date, get_range_of_days)
    url_parts = list(urlparse(url))
    params = dict(parse_qsl(url_parts[4]))
    return datetime.strptime(params[key], date_format())

@pytest.mark.parametrize(["start_date", "get_range_of_days", "key"], [
    [datetime(year=2026, month=3, day=27), False, "date_echeance"],
    [datetime(year=2026, month=3, day=26), False, "date_echeance"],
    [datetime(year=2025, month=1, day=30), True, "date_debut_echeance"],
])
def test_date(start_date, get_range_of_days, key):
    assert get_param(start_date, get_range_of_days, key) == start_date

def test_default_date():
    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    assert get_param(None, None, "date_echeance") == yesterday
    assert get_param(None, True, "date_debut_echeance") == yesterday

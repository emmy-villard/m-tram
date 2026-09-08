from etl.extract.endpoint_url.openmeteo import get_url, date_format
from datetime import datetime, timedelta
import pytest
from urllib.parse import urlparse, parse_qsl
from util.date import date_format
import requests

def test_is_valid_endpoint():
    url = get_url()
    response = requests.get(url)
    assert response.status_code == 200

def get_param(start_date, end_date, key):
    url = get_url(start_date, end_date)
    url_parts = list(urlparse(url))
    params = dict(parse_qsl(url_parts[4]))
    return datetime.strptime(params[key], date_format())

@pytest.mark.parametrize(["start_date", "end_date"], [
    [datetime(year=2026, month=3, day=27), datetime(year=2026, month=3, day=27)],
    [datetime(year=2026, month=3, day=26), datetime(year=2026, month=3, day=27)],
    [datetime(year=2025, month=1, day=30), datetime(year=2026, month=12, day=1)],
])
def test_correct_date(start_date, end_date):
    assert get_param(start_date, end_date, "start_date") == start_date
    assert get_param(start_date, end_date, "end_date") == end_date

@pytest.mark.parametrize(["start_date", "end_date"], [
    [datetime(year=2026, month=3, day=27), datetime(year=2026, month=3, day=26)]
])
def test_incorrect_date(start_date, end_date):
    with pytest.raises(ValueError):
        assert get_param(start_date, end_date, "end_date") != start_date

def test_default_date():
    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    assert get_param(None, None, "start_date") == yesterday

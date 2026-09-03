from etl.extract.api_url import url_openapi_meteo, date_format
from datetime import datetime
import pytest
from urllib.parse import urlparse, parse_qsl

@pytest.fixture
def date():
    return datetime(year=2026, month=3, day=27)

@pytest.fixture
def query(date):
    url = url_openapi_meteo(date)
    url_parts = list(urlparse(url))
    return dict(parse_qsl(url_parts[4]))

@pytest.mark.parametrize("key", ["start_date", "end_date"])
def test_date(key, query, date):
    assert datetime.strptime(query[key], date_format()) == date
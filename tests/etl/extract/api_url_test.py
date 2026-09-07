from etl.extract.api_url import url_openapi_meteo, date_format
from datetime import datetime
import pytest
from urllib.parse import urlparse, parse_qsl
from etl.extract.url_util import date_format

def get_param(start_date, end_date, key):
    url = url_openapi_meteo(start_date, end_date)
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
        get_param(start_date, end_date, "start_date")

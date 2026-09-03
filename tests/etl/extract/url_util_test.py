from datetime import datetime
from etl.extract.url_util import update_url_params
import pytest

@pytest.fixture
def base_url():
    return "localhost/?id=3"

@pytest.fixture
def params():
    return {
        "user": "7",
        "animal": "cat",
    }

@pytest.fixture
def end_url():
    return "localhost/?id=3&user=7&animal=cat"


def test_update_url_params(base_url, params, end_url):
    assert update_url_params(base_url, params) == end_url
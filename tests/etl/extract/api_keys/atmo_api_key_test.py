from etl.extract.api_keys.atmo import get_api_key

def test_key_exists():
    assert get_api_key() != ""
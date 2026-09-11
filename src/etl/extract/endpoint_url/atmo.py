from etl.extract.api_keys.atmo import get_api_key
from util.url import update_url_params
from datetime import datetime, timedelta
from util.date import date_format

def get_url(
        date: datetime=datetime.now()-timedelta(days=1),
        get_range_of_days=False
):
    base_url = "https://api.atmo-aura.fr/api/v1/communes/38185/indices/atmo"
    params = {
        "api_token": get_api_key(),
    }
    date_str = date.strftime(date_format())
    if get_range_of_days:
        params["date_debut_echeance"] = date_str
    else:
        params["date_echeance"] = date_str
    return update_url_params(base_url, params)
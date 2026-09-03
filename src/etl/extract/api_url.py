from datetime import datetime
from etl.extract.url_util import date_format, update_url_params

"""
URLs of APIs endpoints
"""
url_ligne = "https://data.mobilites-m.fr/api/dyn/ligne/json"
url_trr = "https://data.mobilites-m.fr/api/dyn/trr/json"

def url_openapi_meteo(day: datetime):
    """
    Return fetch URL of a given day for the Open Meteo API

    Parameters
    ----------
    day : datetime
        Datetime of the day to fetch.

    Returns
    -------
    string
        url to fetch
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    date_str = day.strftime(date_format())
    lat_grenoble, long_grenoble = '45.17', '5.72'
    data_requested = 'temperature_2m,apparent_temperature,' \
        'relativehumidity_2m,precipitation,rain,snowfall,weathercode,' \
        'pressure_msl,cloudcover,windspeed_10m,windgusts_10m'
    params = {
        'latitude': lat_grenoble,
        'longitude': long_grenoble,
        'start_date': date_str,
        'end_date': date_str,
        'hourly': data_requested,
        'timezone': 'Europe/Paris',
    }
    return update_url_params(url, params)
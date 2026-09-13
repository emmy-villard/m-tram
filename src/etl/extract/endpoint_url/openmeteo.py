from datetime import datetime, timedelta
from util.date import date_format
from util.url import update_url_params

def get_url(
    start_date: datetime=datetime.now() - timedelta(days=1),
    end_date: datetime=datetime.now() - timedelta(days=1)
):
    """
    Return fetch URL of a given day for the Open Meteo API

    Parameters
    ----------
    start_date : datetime
        Datetime of the first day to fetch.
    end_date : datetime
        Datetime of the last day to fetch.

    Returns
    -------
    string
        url to fetch
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    if not start_date:
        start_date = datetime.now() - timedelta(days=1)
    if not end_date:
        end_date = datetime.now() - timedelta(days=1)
    if ((end_date - start_date).days < 0):
        raise ValueError("start_date must be before end_date")
    start_date_str = start_date.strftime(date_format())
    end_date_str = end_date.strftime(date_format())
    lat_grenoble, long_grenoble = '45.17', '5.72'
    data_requested = 'temperature_2m,apparent_temperature,' \
        'relativehumidity_2m,precipitation,rain,snowfall,weathercode,' \
        'pressure_msl,cloudcover,windspeed_10m,windgusts_10m'
    params = {
        'latitude': lat_grenoble,
        'longitude': long_grenoble,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'hourly': data_requested,
        'timezone': 'Europe/Paris',
    }
    return update_url_params(url, params)
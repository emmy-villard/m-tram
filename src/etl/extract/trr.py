import requests

def fetch_trr():
    """
    Get raw json dynamic data from MData API "trr"

    Parameters
    ----------

    Returns
    -------
    dictionnary
        Raw json trr data
    """
    url_ttr = "https://data.mobilites-m.fr/api/dyn/trr/json"
    response_ttr = requests.get(url_ttr)
    return response_ttr.json()
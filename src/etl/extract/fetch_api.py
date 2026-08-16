import requests

def fetch_api(url):
    """
    Get raw json dynamic data from open APIs

    Parameters
    ----------
    url : string
        API endpoint to fetch

    Returns
    -------
    dictionnary
        Raw json data
    """
    response = requests.get(url)
    return response.json()
import requests
import logging

logger = logging.getLogger(__name__)
def fetch_mdata_api(url):
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
    logger.info(f"Fetching {url}")
    response = requests.get(url)
    logger.info(f"Response code: {response.status_code}")
    return response.json()
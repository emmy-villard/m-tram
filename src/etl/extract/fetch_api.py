import requests
import logging

logger = logging.getLogger(__name__)

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
    logger.info(f"Fetching {url}")
    response = requests.get(url, timeout=30)
    logger.info(f"Response code: {response.status_code}")
    response.raise_for_status()
    return response.json()
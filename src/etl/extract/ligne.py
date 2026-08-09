import requests

def fetch_ligne():
    """
    Get raw json dynamic data from MData API "ligne"

    Parameters
    ----------

    Returns
    -------
    dictionnary
        Raw json ligne data
    """
    url_ligne = "https://data.mobilites-m.fr/api/dyn/ligne/json"
    reponse_ligne = requests.get(url_ligne)
    return reponse_ligne.json()
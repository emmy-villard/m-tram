def get_url():
    """
    Return fetch URL of dynamic MData for tram lines

    Returns
    -------
    string
        url to fetch
    """
    base_url = "https://data.mobilites-m.fr/api/dyn/ligne/json"
    return base_url
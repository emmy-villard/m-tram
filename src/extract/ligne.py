import requests
import pandas as pd

def fetch_ligne():
    url_ttr = "https://data.mobilites-m.fr/api/dyn/ligne/json"
    response_ttr = requests.get(url_ttr)
    return response_ttr.json()
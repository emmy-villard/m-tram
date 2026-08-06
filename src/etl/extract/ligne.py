import requests

def fetch_ligne():
    url_ligne = "https://data.mobilites-m.fr/api/dyn/ligne/json"
    reponse_ligne = requests.get(url_ligne)
    return reponse_ligne.json()
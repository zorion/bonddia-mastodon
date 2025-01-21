import requests
URL_SOURCE = 'http://www.rogerdarlington.me.uk/Goodmorning.html'

def get_text():
    response = requests.get(URL_SOURCE)
    response.raise_for_status()
    return response.text

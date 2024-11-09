import os
import requests

# Variables d'entorn
API_BASE_URL = os.getenv("MASTODON_API_BASE_URL")
ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")


def envia(missatge):
    url = f"{API_BASE_URL}/api/v1/statuses"

    # Headers per l'autenticació
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    data = {"status": missatge}

    # Enviar el toot
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("Tot bé!")
    else:
        print(f"Error a l'enviar el tut: {response.status_code}")
        print(response.json())


if __name__ == "__main__":
    missatge = "BONDDIA"
    envia(missatge)

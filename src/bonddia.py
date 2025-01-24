from __future__ import annotations
import os
import random

import requests

# Variables d'entorn
API_BASE_URL = os.getenv("MASTODON_API_BASE_URL")
ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")


def envia(missatge: str):
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


def obtenir_missatge(text: str, idioma: str) -> str:
    missatge = f"""{text}

#BonDia
Idioma: #{idioma}
#BondDia
    """
    print(f"Missatge: ----\n{missatge}\n-------------------")
    return missatge


def selecciona_idioma(traduccions: dict[str]) -> tuple[str, str]:
    idiomes = list(traduccions.keys())
    idioma = random.choice(idiomes)
    return idioma, traduccions[idioma]


def obtenir_traduccions() -> str:
    try:
        from .lang import get_langs

        return get_langs()
    except Exception as err:
        print(f"Error aconseguint les traduccions: {err}")
        return {"catalan": "Bon dia"}


if __name__ == "__main__":
    traduccions = obtenir_traduccions()
    idioma, bondia = selecciona_idioma(traduccions)
    missatge = obtenir_missatge(text=bondia, idioma=idioma)
    envia(missatge)

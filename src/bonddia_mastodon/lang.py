import json
from html.parser import HTMLParser

import requests

URL_SOURCE = "http://www.rogerdarlington.me.uk/Goodmorning.html"
CACHE_WEB = "bondia.html"
CACHE_PARSED = "data.json"


def download_source():
    try:
        response = requests.get(URL_SOURCE)
        response.raise_for_status()
        text = response.text
        with open(CACHE_WEB, "w") as f:
            f.write(text)
    except Exception as err:
        print(f"Error baixant el document: {err}, fent servir cache.")
        with open(CACHE_WEB, "r") as f:
            text = f.read()
    return text


def get_langs():
    try:
        with open(CACHE_PARSED, "rb") as f:
            langs = json.load(f)
        print("Got langs from cache")
    except FileNotFoundError:
        text = download_source()
        langs = parse_lang(text)
        with open(CACHE_PARSED, "wb") as f:
            json.dump(langs, f, indent=4)
        print("Downloaded langs:", langs)
    return langs


def parse_lang(text):
    lp = LangParser()
    lp.feed(text)
    result = lp.get_result()

    return result


STATUS_INITIAL = "Abans de la taula"
STATUS_READING = "Llegint"
STATUS_GETTING_LANG = "Llegint nou idioma"
STATUS_LANGUAGE_GOT = "Llegint per al idioma"
STATUS_FINISHED = "Acabada la taula"


class LangParser(HTMLParser):
    def __init__(self):
        self.__status = STATUS_INITIAL
        self.__lang = None
        self.__result = {}
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == "table" and self.__status == STATUS_INITIAL:
            self.__status = STATUS_READING
        if tag == "td":
            if self.__status == STATUS_READING:
                self.__status = STATUS_GETTING_LANG
            elif self.__status == STATUS_GETTING_LANG:
                self.__status = STATUS_LANGUAGE_GOT
                assert self.__lang is not None

    def handle_endtag(self, tag):
        if tag == "table":
            self.__status = STATUS_FINISHED

    def handle_data(self, data):
        if self.__status == STATUS_LANGUAGE_GOT:
            lang = self.__lang.strip()
            bondia = data.strip()
            self.__result[lang] = bondia
            self.__lang = None
            self.__status = STATUS_READING

        if self.__status == STATUS_GETTING_LANG:
            assert self.__lang is None
            self.__lang = data

    def get_result(self):
        return self.__result

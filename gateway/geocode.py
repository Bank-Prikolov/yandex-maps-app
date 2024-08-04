import requests

from config import YandexApisConfig
from misc import format_lang


def get_toponym(language, place_name=None, coords=None):
    lang = format_lang(language)
    geocode_params = {
        'apikey': YandexApisConfig.GEOCODE_API_KEY,
        'lang': lang,
        'format': 'json',
    }
    if place_name:
        geocode_params['geocode'] = place_name
    else:
        geocode_params['geocode'] = coords
    geocode_api_server = 'http://geocode-maps.yandex.ru/1.x'
    response = requests.get(geocode_api_server, params=geocode_params, timeout=300)
    return response

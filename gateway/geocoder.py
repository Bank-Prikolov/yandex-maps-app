import requests

from config import YandexApisConfig
from misc import format_lang


def get_toponym(language, place_name=None, coords=None):
    lang = format_lang(language)
    geocoder_params = {
        'apikey': YandexApisConfig.GEOCODER_API_KEY,
        'lang': lang,
        'format': 'json',
    }
    if place_name:
        geocoder_params['geocode'] = place_name
    else:
        geocoder_params['geocode'] = coords
    geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x'
    response = requests.get(geocoder_api_server, params=geocoder_params, timeout=300)
    return response

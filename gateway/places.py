import requests

from config import YandexApisConfig
from misc import format_lang


def get_organization(coords, text, language):
    lang = format_lang(language)
    if coords is not None:
        places_params = {
            'apikey': YandexApisConfig.PLACES_API_KEY,
            'text': str(text),
            'lang': lang,
            'll': coords,
            'type': 'biz',
            'rspn': 1,
            'results': 1,
        }
    else:
        places_params = {
            'apikey': YandexApisConfig.PLACES_API_KEY,
            'text': str(text),
            'lang': lang,
            'type': 'biz',
            'rspn': 1,
            'results': 1,
        }
    places_api_server = 'http://search-maps.yandex.ru/v1/'
    response = requests.get(places_api_server, params=places_params, timeout=300)
    return response

import requests

from config import YandexApisConfig
from misc import format_lang


def get_organization(coords, text, language):
    lang = format_lang(language)
    if coords is not None:
        search_params = {
            'apikey': YandexApisConfig.SEARCH_API_KEY,
            'text': str(text),
            'lang': lang,
            'll': coords,
            'type': 'biz',
            'rspn': 1,
            'results': 1,
        }
    else:
        search_params = {
            'apikey': YandexApisConfig.SEARCH_API_KEY,
            'text': str(text),
            'lang': lang,
            'type': 'biz',
            'rspn': 1,
            'results': 1,
        }
    search_api_server = 'http://search-maps.yandex.ru/v1/'
    response = requests.get(search_api_server, params=search_params, timeout=300)
    return response

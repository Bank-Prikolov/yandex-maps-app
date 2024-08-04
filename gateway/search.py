import requests

from config import YandexApisConfig


def get_organization(coords, text):
    search_params = {
        'apikey': YandexApisConfig.SEARCH_API_KEY,
        'text': str(text),
        'lang': 'ru_RU',
        'll': coords,
        'type': 'biz',
        'rspn': 1,
        'results': 1,
    }
    search_api_server = 'http://search-maps.yandex.ru/v1/'
    response = requests.get(search_api_server, params=search_params, timeout=300)
    return response

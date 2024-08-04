import requests

from config import YandexApisConfig


def get_toponym(place_name=None, coords=None):
    geocode_params = {
        'apikey': YandexApisConfig.GEOCODE_API_KEY,
        'format': 'json',
    }
    if place_name:
        geocode_params['geocode'] = place_name
    else:
        geocode_params['geocode'] = coords
    geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x'
    response = requests.get(geocoder_api_server, params=geocode_params, timeout=300)
    return response

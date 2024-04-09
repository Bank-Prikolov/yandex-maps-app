import os
import requests
import math
from geopy.distance import geodesic


def get_map(data):
    map_params = {
        'll': ','.join(list(map(str, data.coords))),
        'l': data.display,
        'pt': data.pt,
        'size': '619,429',
        'z': str(data.z),
    }

    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    response = requests.get(map_api_server, params=map_params)
    return response


def get_toponym(place_name=None, coords=None):
    geocoder_params = {
        'apikey': os.getenv('GEOCODER_API_KEY'),
        'format': 'json',
    }
    if place_name:
        geocoder_params['geocode'] = place_name
    else:
        geocoder_params['geocode'] = coords

    geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x'
    response = requests.get(geocoder_api_server, params=geocoder_params)
    return response


def get_organization(coords, text):
    search_params = {
        'apikey': os.getenv('ORGANIZATION_API_KEY'),
        'text': str(text),
        'lang': 'ru_RU',
        'll': coords,
        'type': 'biz',
        'rspn': 1,
        'results': 1,
    }

    search_api_server = 'https://search-maps.yandex.ru/v1/'
    response = requests.get(search_api_server, params=search_params)
    return response


def degrees_to_pixels(coord1, z):
    coordX = 360 / (2 ** (z + 8))
    coordY = math.cos(math.radians(coord1)) * 360 / (2 ** (z + 8))
    return coordX, coordY


def ab_distance(a, b):
    a, b = tuple(a), tuple(b)
    distance = geodesic(a, b).meters
    return distance

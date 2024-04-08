import os
import requests
import math
import main


def get_place_map(data):
    map_params = {
        'll': ','.join(list(map(str, data.coords))),
        'l': data.display,
        'pt': data.pt,
        'size': '619,429',
        'z': str(data.z),
    }

    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    response = requests.get(map_api_server, params=map_params)
    print(response.url)
    return response


def get_place_toponym(place_name=None, coords=None):
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


def get_organization(coords):
    search_params = {
        'apikey': os.getenv('ORGANIZATION_API_KEY'),
        'text': 'organization',
        'lang': 'ru_RU',
        'll': coords,
        'type': 'biz',
        'rspn': 1,
        'results': 1,
    }

    search_api_server = 'https://search-maps.yandex.ru/v1/'
    response = requests.get(search_api_server, params=search_params)
    print(response.json())
    return response


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.0)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance




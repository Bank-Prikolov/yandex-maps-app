import os
import requests
import math
from typing import Union


def get_place_map(data) -> requests.Response:
    map_params = {
        'll': ','.join(list(map(str, data.coords))),
        'l': data.display,
        'spn': f'{data.spn},{data.spn}',
        'pt': data.pt,
        'size': '619,429',
    }

    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    response = requests.get(map_api_server, params=map_params)
    return response


def get_place_toponym(place_name=None, coords=None) -> requests.Response:
    geocoder_params = {
        'apikey': os.getenv('GEOCODER_API_KEY'),
        'format': 'json',
        'islands': 'violetIcon',
    }
    if place_name:
        geocoder_params['geocode'] = place_name
    else:
        geocoder_params['geocode'] = coords

    geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x'
    response = requests.get(geocoder_api_server, params=geocoder_params)
    return response


def get_organization(coords: str) -> requests.Response:
    search_params = {
        'apikey': os.getenv('ORGANIZATION_API_KEY'),
        'text': 'аптека',
        'lang': 'ru_RU',
        'll': coords,
        'type': 'biz',
        'results': 1,
        'rspn': 1,
    }

    search_api_server = 'https://search-maps.yandex.ru/v1/'
    response = requests.get(search_api_server, params=search_params)
    return response


# функция, считающая расстояние между двумя точками по координатам
def lonlat_distance(a: Union[list, tuple], b: Union[list, tuple]) -> float:
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.0)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance

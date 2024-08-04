import requests


def get_map(data):
    static_params = {
        'll': ','.join(list(map(str, data.coords))),
        'l': data.display,
        'pt': data.pt,
        'size': '619,429',
        'z': str(data.z),
    }
    static_api_server = 'https://static-maps.yandex.ru/1.x/'
    response = requests.get(static_api_server, params=static_params, timeout=300)
    return response

import requests


def get_pic(x, y, zoom=18, l='map'):
    x = float(x)
    y = float(y)
    zoom = zoom
    map_request = f"http://static-maps.yandex.ru/1.x/?l={l}&ll={x}%2C{y}&z={zoom}"
    response = requests.get(map_request)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def search(sear4):
    req = requests.get(f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={sear4}&format=json")
    return req.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
              'GeocoderMetaData']['Address']['formatted']

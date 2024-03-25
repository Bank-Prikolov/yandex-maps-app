import requests

lis = ['Хабаровск', 'Уфа', 'Нижний Новгород', 'Калининград']
def act(lis):
    for x in lis:
        response = requests.get(f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=уфа&format=json")
        print(response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
                  'GeocoderMetaData']['Address']['Components'][1]['name'])
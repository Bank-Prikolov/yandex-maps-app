import requests
x = float(input())
y = float(input())
zoom = float(input())
map_request = f"http://static-maps.yandex.ru/1.x/?l=map&ll={x}%2C{y}&z={zoom}"
response = requests.get(map_request)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

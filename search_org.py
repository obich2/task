import requests
import sys
from io import BytesIO
from PIL import Image
from distance import lonlat_distance

toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

json_response = requests.get(geocoder_api_server, params=geocoder_params).json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

address_ll = toponym_longitude + ',' + toponym_lattitude

search_params = {
    "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}
search_api_server = "https://search-maps.yandex.ru/v1/"

response = requests.get(search_api_server, params=search_params)

# Преобразуем ответ в json-объект
json_response = response.json()

# Получаем первую найденную организацию.
organization = json_response["features"][0]
# Часы работы организации.
org_hours = organization['properties']['CompanyMetaData']['Hours']['text']
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Координаты организации.
org_coords = organization['geometry']['coordinates']
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]
# Дистанция между организацей и нашим адресом.
distance = str(round(lonlat_distance(address_ll.split(','), org_coords) / 1000, 2)) + ' км'
print(distance)

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])
delta = "0.009"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address_ll,
    "spn": ",".join([delta, delta]),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "{0},pm2rdm~{1},pm2blm".format(org_point, address_ll)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()
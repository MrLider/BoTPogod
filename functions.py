import requests
import json
import configparser
import requests as req
from functools import lru_cache
from geopy import geocoders
from lib import dict_ya
from pyowm.owm import OWM



read_config = configparser.ConfigParser()
read_config.read("settings.ini")
OWM_TOKEN = read_config['settings']['token_owm'].strip().replace(" ", "")  # Токен QWM
owm = OWM(OWM_TOKEN)

#Функция вычисление координат
@lru_cache(maxsize=None)
def geo_pos(city: str):
    geolocator = geocoders.Nominatim(user_agent="telebot")
    latitude = str(geolocator.geocode(city).latitude)
    longitude = str(geolocator.geocode(city).longitude)
    return latitude, longitude

# Функция запроса погоды с сервера яндекс
def yandex_weather(latitude, longitude, city, token_yandex: str):
    url = f"https://api.weather.yandex.ru/v2/informers?lat={latitude}&lon={longitude}"
    headers = {"X-Yandex-API-Key": token_yandex}
    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        data = json.loads(r.text)
        fact = data["fact"]
        condition = dict_ya(fact["condition"])
        post = f' Погодный сервер Яндекс: \n'
        post += f'В населённом пункте {city} сейчас {condition}  \n'
        post += f'Температура в районе {fact["temp"]} °С'
    else:
        post = f'На сегодня достаточно.\n Погодный сервер Яндекс устал!'
    return post

# Функция запроса погоды с сервера OWM
def owm_wather(city: str):
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    observation.weather.detailed_status
    w = observation.weather
    temp = w.temperature('celsius')["temp"]
    post = f'\n\n Погодный сервер OpenWeather: \n'
    post += f'В населенном пункте {city} сейчас {str(w.detailed_status)} \n'
    post += f'Температура в районе {str(round(temp))} °С \n\n'

    return post

#Функция запроса погоды с сервера AuuWeather
def acuu_weather(city: str, code_loc: str, token_accu: str):
    url_weather = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{code_loc}?' \
                  f'apikey={token_accu}&language=ru&metric=True'
    response = req.get(url_weather, headers={"APIKey": token_accu})
    json_data = json.loads(response.text)
    dict_weather = dict()
    dict_weather['link'] = json_data[0]['MobileLink']
    time = 'сейчас'
    dict_weather[time] = {'temp': json_data[0]['Temperature']['Value'], 'sky': json_data[0]['IconPhrase']}
    # for i in range(1, len(json_data)):
    #     time = 'через' + str(i) + 'ч'
    #     dict_weather[time] = {'temp': json_data[i]['Temperature']['Value'], 'sky': json_data[i]['IconPhrase']}
    post = f' Погодный сервер AcuuWeather: \n'
    post += f'В населённом пункте {city} сейчас {str(dict_weather["сейчас"]["sky"]).lower()}  \n'
    post += f'Температура в районе {str(round(dict_weather["сейчас"]["temp"]))} °С'
    return post

#Функция запроса кода населёного пункта

def code_location(latitude, longitude, token_accu: str):
    try:
        url_location_key = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=' \
                       f'{token_accu}&q={latitude},{longitude}&language=ru'
        resp_loc = req.get(url_location_key, headers={"APIKey": token_accu})
        json_data = json.loads(resp_loc.text)
        code = json_data['Key']
    except KeyError:
        code = None
    return code
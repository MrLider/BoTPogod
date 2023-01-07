import requests
import json
import configparser
from geopy import geocoders
from lib import dict
from pyowm.owm import OWM


read_config = configparser.ConfigParser()
read_config.read("settings.ini")
OWM_TOKEN = read_config['settings']['token_owm'].strip().replace(" ", "")  # Токен QWM
owm = OWM(OWM_TOKEN)

def geo_pos(city: str):
    geolocator = geocoders.Nominatim(user_agent="telebot")
    latitude = str(geolocator.geocode(city).latitude)
    longitude = str(geolocator.geocode(city).longitude)
    return latitude, longitude

def yandex_weather(latitude, longitude, city, token_yandex: str):
    url = f"https://api.weather.yandex.ru/v2/informers?lat={latitude}&lon={longitude}"
    headers = {"X-Yandex-API-Key": token_yandex}
    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        data = json.loads(r.text)
        fact = data["fact"]
        condition = dict(fact["condition"])
        post = f' Погодный сервер Яндекс: \n'
        post += f'В населённом пункте {city} сейчас {condition}  \n'
        post += f'Температура в районе {fact["temp"]} °С'
    else:
        post = f'На сегодня достаточно.\n Погодный сервер Яндекс устал!'
    return post
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


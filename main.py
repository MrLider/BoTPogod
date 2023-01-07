import configparser
import telebot
import pyowm
import requests
import json
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError
from telebot import types
from lib import dict

read_config = configparser.ConfigParser()
read_config.read("settings.ini")
BOT_TOKEN = read_config['settings']['token'].strip().replace(" ", "")  # Токен бота
OWM_TOKEN = read_config['settings']['token_owm'].strip().replace(" ", "")  # Токен бота

# Переменные
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM(OWM_TOKEN)
bot = telebot.TeleBot(BOT_TOKEN)


# Обработчик команды старт
@bot.message_handler(commands=['start'])
def echo_all(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    lesogorsk = types.KeyboardButton("Лесогорск")
    moscow = types.KeyboardButton("Москва")
    chsinau = types.KeyboardButton("Кишинёв")
    sochi = types.KeyboardButton("Сочи")
    other = types.KeyboardButton("Другой")
    markup.add( moscow, sochi, chsinau,  lesogorsk, other)
    bot.send_message(message.chat.id, "Выберите населённый пункт", reply_markup=markup)

@bot.message_handler()
# Обработчик сервер Яндекс
def main(message):
    if message.text == "Лесогорск":
        url = "https://api.weather.yandex.ru/v2/informers?lat=56.05305&lon=99.53259"
        headers = {"X-Yandex-API-Key": "81b5d261-4e19-4848-adad-36cc71ddcf4d"}
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            data = json.loads(r.text)
            fact = data["fact"]
            condition = dict(fact["condition"])
            post = f' Погодный сервер Яндекс: \n'
            post += f'В населённом пункте {message.text} сейчас {condition}  \n'
            post += f'Температура в районе {fact["temp"]} °С'
        else:
            post = f'На сегодня достаточно.\n Погодный сервер Яндекс устал!'
    elif message.text == "Москва":
        url = "https://api.weather.yandex.ru/v2/informers?lat=55.67827&lon=37.53719"
        headers = {"X-Yandex-API-Key": "81b5d261-4e19-4848-adad-36cc71ddcf4d"}
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            data = json.loads(r.text)
            fact = data["fact"]
            condition = dict(fact["condition"])
            post = f' Погодный сервер Яндекс: \n'
            post += f'В населённом пункте {message.text} сейчас {condition}  \n'
            post += f'Температура в районе {fact["temp"]} °С'
        else:
            post = f'На сегодня достаточно.\n Погодный сервер Яндекс устал!'
    elif message.text == "Кишинёв":
        url = "https://api.weather.yandex.ru/v2/informers?lat=46.88650&lon=28.99194"
        headers = {"X-Yandex-API-Key": "81b5d261-4e19-4848-adad-36cc71ddcf4d"}
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            data = json.loads(r.text)
            fact = data["fact"]
            condition = dict(fact["condition"])
            post = f' Погодный сервер Яндекс: \n'
            post += f'В населённом пункте {message.text} сейчас {condition}  \n'
            post += f'Температура в районе {fact["temp"]} °С'

        else:
            post = f'На сегодня достаточно.\n Погодный сервер Яндекс устал!'
    elif message.text == "Сочи":
        url = "https://api.weather.yandex.ru/v2/informers?lat=43.59316&lon=39.72745"
        headers = {"X-Yandex-API-Key": "81b5d261-4e19-4848-adad-36cc71ddcf4d"}
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            data = json.loads(r.text)
            fact = data["fact"]
            condition = dict(fact["condition"])
            post = f' Погодный сервер Яндекс: \n'
            post += f'В населённом пункте {message.text} сейчас {condition}  \n'
            post += f'Температура в районе {fact["temp"]} °С'
        else:
            post = f'На сегодня достаточно.\n Погодный сервер Яндекс устал!'
    else:
        post = ""

    other(message)
    bot.send_message(message.chat.id, post)

# Обработчик сервер OpenWeather
def other(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    lesogorsk = types.KeyboardButton("Лесогорск")
    moscow = types.KeyboardButton("Москва")
    chsinau = types.KeyboardButton("Кишинёв")
    sochi = types.KeyboardButton("Сочи")
    other = types.KeyboardButton("Другой")

    markup.add( moscow, sochi, chsinau,  lesogorsk, other)

    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(message.text)
        observation.weather.detailed_status
        w = observation.weather
        temp = w.temperature('celsius')["temp"]
        post = f'\n\n Погодный сервер OpenWeather: \n'
        post += f'В населенном пункте {message.text} сейчас {str(w.detailed_status)} \n'
        post += f'Температура в районе {str(round(temp))} °С \n\n'

    except NotFoundError:

        post = "Введите название населённого пункта"
    bot.send_message(message.chat.id, post, reply_markup=markup)

bot.polling(none_stop = True)
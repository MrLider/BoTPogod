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
from functions import yandex_weather, geo_pos, owm_wather


read_config = configparser.ConfigParser()
read_config.read("settings.ini")
BOT_TOKEN = read_config['settings']['token'].strip().replace(" ", "")  # Токен бота

YA_TOKEN = read_config['settings']['token_yandex'].strip().replace(" ", "")  # Токен Yandex

# Переменные
config_dict = get_default_config()
config_dict['language'] = 'ru'
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
        lat = 56.05305
        lon = 99.53259
        post = yandex_weather(lat, lon, message.text, YA_TOKEN)
    elif message.text == "Москва":
        lat = 55.67827
        lon = 37.53719
        post = yandex_weather(lat, lon, message.text, YA_TOKEN)
    elif message.text == "Кишинёв":
        lat = 46.88650
        lon = 28.99194
        post = yandex_weather(lat, lon, message.text, YA_TOKEN)

    elif message.text == "Сочи":
        lat = 43.593232
        lon = 39.727434
        post = yandex_weather(lat, lon, message.text, YA_TOKEN)
    elif message.text == "Другой":

        post = ""
    else:
        lat = geo_pos(message.text)[0]
        lon = geo_pos(message.text)[1]
        post = yandex_weather(lat, lon, message.text, YA_TOKEN)


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
    try:
        post = owm_wather(message.text)
    except NotFoundError:
        post = "Введите название населённого пункта"


    bot.send_message(message.chat.id, post, reply_markup=markup)

bot.polling(none_stop = True)
import configparser
import telebot
import os, sys
from requests.exceptions import ConnectionError, ReadTimeout
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError
from telebot import types
from functions import yandex_weather, geo_pos, owm_wather, code_location, acuu_weather

# Переменные
read_config = configparser.ConfigParser()
read_config.read("settings.ini")
BOT_TOKEN = read_config['settings']['token'].strip().replace(" ", "")  # Токен бота
YA_TOKEN = read_config['settings']['token_yandex'].strip().replace(" ", "")  # Токен Yandex
ACUU_TOKEN = read_config['settings']['token_acuu'].strip().replace(" ", "")  # Токен Yandex


config_dict = get_default_config()
config_dict['language'] = 'ru'
bot = telebot.TeleBot(BOT_TOKEN)

# Кнопки меню
markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
lesogorsk = types.KeyboardButton("Лесогорск")
moscow = types.KeyboardButton("Москва")
chsinau = types.KeyboardButton("Кишинёв")
sochi = types.KeyboardButton("Сочи")
other = types.KeyboardButton("Другой")
markup.add(moscow, sochi, chsinau, lesogorsk, other)

# Обработчик команды старт
@bot.message_handler(commands=['start'])
def echo_all(message):
    bot.send_message(message.chat.id, "Выберите населённый пункт", reply_markup=markup)

@bot.message_handler()
# Обработчик сообщений
def main(message):
    if message.text == "Лесогорск":
        lat = '56.05305'
        lon = '99.53259'
        post_ya = yandex_weather(lat, lon, message.text, YA_TOKEN)
        post_owm = owm_wather(message.text)
        code_loc = code_location(lat, lon, ACUU_TOKEN)
        if code_loc is None:
            post_acuu = None
        else:
            post_acuu = acuu_weather(message.text, code_loc, ACUU_TOKEN)

    elif message.text == "Москва":
        lat = '55.67827'
        lon = '37.53719'
        post_ya = yandex_weather(lat, lon, message.text, YA_TOKEN)
        post_owm = owm_wather(message.text)
        code_loc = code_location(lat, lon, ACUU_TOKEN)
        if code_loc is None:
            post_acuu = None
        else:
            post_acuu = acuu_weather(message.text, code_loc, ACUU_TOKEN)


    elif message.text == "Кишинёв":
        lat = '46.88650'
        lon = '28.99194'
        post_ya = yandex_weather(lat, lon, message.text, YA_TOKEN)
        post_owm = owm_wather(message.text)
        code_loc = code_location(lat, lon, ACUU_TOKEN)

        if code_loc is None:
            post_acuu = None
        else:
            post_acuu = acuu_weather(message.text, code_loc, ACUU_TOKEN)


    elif message.text == "Сочи":
        lat = '43.593232'
        lon = '39.727434'
        post_ya = yandex_weather(lat, lon, message.text, YA_TOKEN)
        post_owm = owm_wather(message.text)
        code_loc = code_location(lat, lon, ACUU_TOKEN)
        if code_loc is None:
            post_acuu = None
        else:
            post_acuu = acuu_weather(message.text, code_loc, ACUU_TOKEN)

    elif message.text == "Другой":
        post_owm = f"Введите название населённого пункта: "
        post_ya = None
        post_acuu = None

    else:
        try:
            lat, lon  = geo_pos(message.text)
            post_ya = yandex_weather(lat, lon, message.text, YA_TOKEN)
            post_owm = owm_wather(message.text)
            code_loc = code_location(lat, lon, ACUU_TOKEN)
            if code_loc is None:
                post_acuu = None
            else:
                post_acuu = acuu_weather(message.text, code_loc, ACUU_TOKEN)

            print(geo_pos.cache_info())
        except NotFoundError:
            post_owm = f"Населённый пункт не найден"
            post_ya = f"Введите название населённого пункта:"
            post_acuu = None
        except AttributeError:
            post_owm = f"Населённый пункт не найден"
            post_ya = f"Введите название населённого пункта:"
            post_acuu = None
        except  UnboundLocalError:
            post_owm = f"Населённый пункт не найден"
            post_ya = f"Введите название населённого пункта:"
            post_acuu = None

    if post_acuu is None and post_ya is None:
        bot.send_message(message.chat.id, post_owm)
    elif post_ya is None:
        bot.send_message(message.chat.id, post_owm)
        bot.send_message(message.chat.id, post_acuu)
    elif post_acuu is None:
        bot.send_message(message.chat.id, post_owm)
        bot.send_message(message.chat.id, post_ya)

    else:
        bot.send_message(message.chat.id, post_owm)
        bot.send_message(message.chat.id, post_ya)
        bot.send_message(message.chat.id, post_acuu, reply_markup=markup)

try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from telebot import TeleBot

owm = OWM("OWM_TOKEN")
bot = TeleBot("TELEGRAM_TOKEN")

city = 'Тирасполь'

config_dict = get_default_config()
config_dict['language'] = 'RU'

mgr = owm.weather_manager()
observation = mgr.weather_at_place(city)
w = observation.weather


@bot.message_handler(commands=['start'])
def reply(message):
    bot.send_message(message.chat.id,
                     'Привет, я могу предоставить тебе сведения о погоде в Тирасполе'
                     ' на данный момент! Напиши мне "погода"!')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    if message.text.lower() == 'погода':
        bot.send_message(message.chat.id,
                         f"""Сведения о погоде:
Город: {city}
Температура: {w.temperature('celsius').get('temp')}°C
Ощущается как: {w.temperature('celsius').get('feels_like')}
Давление: {int(w.pressure.get('press') / 1.333)} мм рт. ст.
Скорость ветра: {w.wind()['speed']} м/c
Влажность: {w.humidity}%
Облачность: {w.clouds}%
Статус: {w.detailed_status}
"""
                         )
    else:
        bot.send_message(message.chat.id, 'Напиши "погода"!')


if __name__ == "__main__":
    bot.polling(none_stop=True)

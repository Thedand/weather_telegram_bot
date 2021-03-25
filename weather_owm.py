from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from telebot import TeleBot

owm = OWM("OWM_TOKEN")
bot = TeleBot("TELEGRAM_TOKEN")

config_dict = get_default_config()
config_dict['language'] = 'RU'

mgr = owm.weather_manager()


@bot.message_handler(commands=['start'])
def reply(message):
    bot.send_message(message.chat.id,
                     'Привет, я могу предоставить тебе сведения о погоде в твоём городе,'
                     ' напиши его!')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    try:
        city = message.text.lower()
        observation = mgr.weather_at_place(city)
        w = observation.weather
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
    except:
        bot.send_message(message.chat.id, 'Возможно ты ошибься, попробуй ввести другой город!')


if __name__ == "__main__":
    bot.polling(none_stop=True)

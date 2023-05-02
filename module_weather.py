from datetime import datetime, timezone, timedelta
import requests
from config import OPEN_WEATHER_TOKEN
# from pprint import pprint


CODE_TO_EMOJI = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}

def get_weather(city, token):
    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={OPEN_WEATHER_TOKEN}")
        data = r.json()
        # pprint(data)
        
        msk_time = datetime.fromtimestamp(data['dt'], timezone(timedelta(hours=3))).strftime('%d-%m-%Y %H:%M:%S')
        city = data['name']
        country = data['sys']['country']
        weather_desc = data['weather'][0]['description']
        temp_cur = data['main']['temp']
        temp_feels_like = data['main']['feels_like']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        humidity = data['main']['humidity']
        pressure = round((data['main']['pressure']/1.333), 1)
        wind_speed = data['wind']['speed']
        sunrise_timestamp = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'])
        msk_sunrise_timestamp = datetime.fromtimestamp(data['sys']['sunrise'], timezone(timedelta(hours=3))).strftime('%d-%m-%Y %H:%M:%S')
        msk_sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'], timezone(timedelta(hours=3))).strftime('%d-%m-%Y %H:%M:%S')
        length_of_the_day = sunset_timestamp - sunrise_timestamp
        
        weather_main = data['weather'][0]['main']
        if weather_main in CODE_TO_EMOJI:
            wm = CODE_TO_EMOJI[weather_main]
        else:
            wm = "Что-то необычное. Лучше посмотри в окно"

        data1 = f"""
<b>Погода на {msk_time} (МСК):</b>
Погода в городе: {country}, {city} - {weather_desc} ({wm})
Температура: {temp_cur}°C
Ощущается как: {temp_feels_like}°C
Максимальная температура: {temp_max}°C
Минимальная температура: {temp_min}°C
Влажность: {humidity}%
Давление: {pressure} мм.рт.ст.
Скорость ветра: {wind_speed} м/c
Восход: {msk_sunrise_timestamp} (МСК)
Закат: {msk_sunset_timestamp} (МСК)
Продолжительность дня: {length_of_the_day}\n
<b>Хорошего дня!</b> ❤️
        """
        return data1
    except Exception as ex:
        return f"""
⚠️ Города с именем <b>{city}</b> не найдено ⚠️
{ex.__class__.__name__}: {ex}
"""

def get_forecast_weather(city, OPEN_WEATHER_TOKEN, count):
    datas = []
    try:
        # за 5 дней с шагом 3 часа, где cnt - количество шагов
        r = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={OPEN_WEATHER_TOKEN}&lang=ru&cnt={count}")
        data = r.json()

        for i in range(count):
            msk_time = datetime.fromtimestamp(data['list'][i]['dt'], timezone(timedelta(hours=3))).strftime('%d-%m-%Y %H:%M:%S')
            city = data['city']['name']
            country = data['city']['country']
            weather_desc = data['list'][i]['weather'][0]['description']
            temp_cur = data['list'][i]['main']['temp']
            temp_feels_like = data['list'][i]['main']['feels_like']
            temp_max = data['list'][i]['main']['temp_max']
            temp_min = data['list'][i]['main']['temp_min']
            humidity = data['list'][i]['main']['humidity']
            pressure = round((data['list'][i]['main']['pressure']/1.333), 1)
            wind_speed = data['list'][i]['wind']['speed']
            weather_main = data['list'][i]['weather'][0]['main']

            if weather_main in CODE_TO_EMOJI:
                wm = CODE_TO_EMOJI[weather_main]
            
            data1 = f"""
*****№{i+1}*****
<b>Погода на {msk_time} (МСК):</b>
Погода в городе: {country}, {city} - {weather_desc} ({wm})
Температура: {temp_cur}°C
Ощущается как: {temp_feels_like}°C
Максимальная температура: {temp_max}°C
Минимальная температура: {temp_min}°C
Влажность: {humidity}%
Давление: {pressure} мм.рт.ст.
Скорость ветра: {wind_speed} м/c
                """
            datas.append(data1)

        return '\n'.join(datas)
    except IndexError:
        return f"""
Введенное вами количество трехчасовых интервалов превышает максимально допустимое значение в 40. Пожалуйста, введите количество интервалов заново.
"""
    except Exception as ex:
        return f"""
⚠️ Города с именем <b>{city}</b> не найдено ⚠️
{ex.__class__.__name__}: {ex}
"""
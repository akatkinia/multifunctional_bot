from datetime import datetime
import requests
from config import OPEN_WEATHER_TOKEN
# from pprint import pprint


def get_weather(city, token):
    code_to_emoji = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={OPEN_WEATHER_TOKEN}")
        data = r.json()
        # pprint(data)
        
        cur_time = datetime.fromtimestamp(data['dt'])
        city = data['name']
        country = data['sys']['country']
        weather_desc = data['weather'][0]['description']
        temp_cur = data['main']['temp']
        temp_feels_like = data['main']['feels_like']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        sunrise_timestamp = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp
        
        weather_main = data['weather'][0]['main']
        if weather_main in code_to_emoji:
            wm = code_to_emoji[weather_main]
        else:
            wm = "Что-то необычное. Лучше посмотри в окно"

        data1 = f"""
<b>Погода на {cur_time}:</b>
Погода в городе: {country}, {city} - {weather_desc} ({wm})
Температура: {temp_cur}°C
Ощущается как: {temp_feels_like}°C
Максимальная температура: {temp_max}°C
Минимальная температура: {temp_min}°C
Влажность: {humidity}%
Давление: {pressure} мм.рт.ст.
Скорость ветра: {wind_speed} м/c
Восход: {sunrise_timestamp}
Закат: {sunset_timestamp}
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
    code_to_emoji = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        # за 5 дней с шагом 3 часа, где cnt - количество шагов
        r = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={OPEN_WEATHER_TOKEN}&lang=ru&cnt={count}")
        data = r.json()

        if count == 1:
            cur_time = datetime.fromtimestamp(data['list'][count-1]['dt'])
            city = data['city']['name']
            country = data['city']['country']
            weather_desc = data['list'][count-1]['weather'][0]['description']
            temp_cur = data['list'][count-1]['main']['temp']
            temp_feels_like = data['list'][count-1]['main']['feels_like']
            temp_max = data['list'][count-1]['main']['temp_max']
            temp_min = data['list'][count-1]['main']['temp_min']
            humidity = data['list'][count-1]['main']['humidity']
            pressure = data['list'][count-1]['main']['pressure']
            wind_speed = data['list'][count-1]['wind']['speed']
            weather_main = data['list'][count-1]['weather'][0]['main']

            if weather_main in code_to_emoji:
                wm = code_to_emoji[weather_main]
            else:
                wm = "Посмотри в окно, не пойму, что это за погода!"

        elif count > 1:
            for i in range(count):
                cur_time = datetime.fromtimestamp(data['list'][i]['dt'])
                city = data['city']['name']
                country = data['city']['country']
                weather_desc = data['list'][i]['weather'][0]['description']
                temp_cur = data['list'][i]['main']['temp']
                temp_feels_like = data['list'][i]['main']['feels_like']
                temp_max = data['list'][i]['main']['temp_max']
                temp_min = data['list'][i]['main']['temp_min']
                humidity = data['list'][i]['main']['humidity']
                pressure = data['list'][i]['main']['pressure']
                wind_speed = data['list'][i]['wind']['speed']
                weather_main = data['list'][i]['weather'][0]['main']

                if weather_main in code_to_emoji:
                    wm = code_to_emoji[weather_main]
                
                data1 = f"""
*****№{i+1}*****
<b>Погода на {cur_time}:</b>
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
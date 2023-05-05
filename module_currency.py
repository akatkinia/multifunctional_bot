from datetime import datetime
import requests


url = 'https://www.cbr-xml-daily.ru/daily_json.js'
r = requests.get(url)
if r.status_code == 200:
    DATA = r.json()
else:
    raise Exception("Ошибка получения данных")

# Построчно получить пары кода и названия валют
def get_valutes(data=DATA):
# Словарь с парами кода и названия валют
    currencies = {}
    for valute in data['Valute']:
        key = valute
        value = data['Valute'][valute]['Name']
        currencies[key] = value

    result = ""
    for key, value in currencies.items():
        result += f"{key} - {value}\n"
    return f"<b>Список мнемокодов валют</b>:\n{result}\nНапишите мнемокод валюты, курс которой хотите посмотреть."


# Получить текущий курс валюты к рублю
def get_course(key, data=DATA):
    key = key.upper()
    if key in data['Valute']:
        date = datetime.fromisoformat(data['Date']).strftime("%d.%m.%Y %H:%M:%S")
        nominal = data['Valute'][key]['Nominal']
        current = data['Valute'][key]['Value'] / nominal
        previous = data['Valute'][key]['Previous'] / nominal
        current_rub = 1 / current
        previous_rub = 1 / previous
        # diff = "+" + str(round(abs(current - previous), 6)) if current >= previous else "-" + str(round(abs(current - previous), 6))
        diff = f"{current - previous:+0.06f}"
        # diff_rub = "+" + str(round(abs(current_rub - previous_rub), 6)) if current_rub >= previous_rub else "-" + str(round(abs(current_rub - previous_rub), 6))
        diff_rub = f"{current_rub - previous_rub:+0.06f}"
        return f"""💰<b>Курс на дату: {date} (МСК)</b>

Текущий курс {key} к RUB: {current} ({diff})
Вчершний курс {key} к RUB: {previous}

Текущий курс RUB к {key}: {round(current_rub, 6)} ({diff_rub})
Вчершний курс RUB к {key}: {round(previous_rub, 6)}
        """
    else:
        return "Некорректно указан мнемокод валюты. Обратитесь к справке."
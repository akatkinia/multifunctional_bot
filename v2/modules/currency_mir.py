import urllib.request
import ssl
import pdfplumber
import matplotlib.pyplot as plt
from datetime import datetime
import io
import requests
from bs4 import BeautifulSoup as bs


URL = "https://mironline.ru/upload/currency%20rate/FX_rate_Mir.pdf"
FILE_PATH = "MIR.pdf"
COMBINED_TABLE = []

def get_currencies_mir():
    # Создаем объект запроса с отключенной проверкой сертификата
    req = urllib.request.Request(URL, method="GET")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0")
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl._create_unverified_context()))

    # Отправляем запрос и скачиваем файл в память
    response = opener.open(req)
    file_bytes = response.read()

    # Создаем объект файла из байтов
    pdf_file_obj = io.BytesIO(file_bytes)

    # Объединяем таблицы со всех страниц в одну таблицу
    combined_table = []
    with pdfplumber.open(pdf_file_obj) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                # Объединяем таблицы текущей страницы
                for table in tables:
                    combined_table.extend(table)

    # Исключаем элементы с заголовком
    processed_table = [row for row in combined_table if "Валюта Курс Время применения Дата применения" not in row]

    # Преобразуем каждую строку таблицы в словарь
    formatted_data = []
    for row in processed_table:
        row_data = row[0].split(" ")
        valute = ' '.join(row_data[:2])
        currency = row_data[-3]
        time = row_data[-2]
        date = row_data[-1]
        data = {
            "Valute": valute,
            "Currency": currency,
            "Date": date,
            "Time": time
        }
        formatted_data.append(data)
    # print(f"Данные успешно обработаны\n**********")

    return formatted_data

# def get_valutes_mir(main):
def get_valutes_mir(main):
    url = "https://mironline.ru/support/list/kursy_mir/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
    }

    soup = bs(requests.get(url=url, headers=headers).content, "lxml")
    valutes = []

    rows = soup.find("table").find_all("tr")
    for row in rows:
        valute_elem = row.find("p", style="text-align: left;")
        if valute_elem and valute_elem.text.strip() != "Валюта":  # Проверяем наличие элемента и что текст не является пустой строкой и не "Валюта"
            valute = valute_elem.text.strip()
            valutes.append(valute)

    valutes_text = '\n'.join(valutes)

    first_date = main[0]["Date"]
    last_date = main[-1]["Date"]

    # result = f"<b>Доступные валюты:</b>\n{valutes_text}"
    result = f"<b>Доступные валюты:</b>\n{valutes_text}\n\n<b>Диапазон дат, за которые имеются данные:</b>\n{first_date} - {last_date}"

    return result

def get_course_on_date_mir(main, valute, date):
    valute = valute
    date = date

    for data in main:
        if valute == data["Valute"] and date == data["Date"]:
            currency = float(data["Currency"].replace(",", "."))
            time = data["Time"]
            return f"""Курс за {date} {time}
RUB к {valute}: {round(1/currency, 4)}
{valute} к RUB: {currency}
"""
    return f"За выбранную дату нет данных, либо валюта указана некорректно."


def draw_currency_chart_mir(main, valute, start_date, end_date):
    start_date = datetime.strptime(start_date, "%d.%m.%Y")
    end_date = datetime.strptime(end_date, "%d.%m.%Y")

    dates = []
    rates = []
    rates_rub = []

    for data in main:
        date = datetime.strptime(data["Date"], "%d.%m.%Y")
        if valute == data["Valute"] and start_date <= date <= end_date:
            dates.append(data["Date"])
            currency = float(data["Currency"].replace(",", "."))
            currency_rub = 1 / float(data["Currency"].replace(",", "."))

            rates.append(float(data["Currency"].replace(",", ".")))
            rates_rub.append(currency_rub)

    if len(dates) > 0:
        fig1, ax1 = plt.subplots()
        plt.plot(list(reversed(dates)), list(reversed(rates_rub)))
        plt.xlabel("Date")
        plt.ylabel(f"Рублей")
        plt.title(f"Курс рубля к {valute}")
        plt.xticks(rotation=45)
        plt.grid(True)
        # plt.show()

        # Сохраняем первый график в байтовый объект
        bytes_io1 = io.BytesIO()
        plt.savefig(bytes_io1, format='png', dpi=300)
        bytes_io1.seek(0)
        fig1_bytes = bytes_io1.getvalue()

        plt.close(fig1)  # Закрываем первый график

        fig2, ax2 = plt.subplots()
        plt.plot(list(reversed(dates)), list(reversed(rates)))
        plt.xlabel("Date")
        plt.ylabel(valute)
        plt.title(f"Курс {valute} к рублю")
        plt.xticks(rotation=45)
        plt.grid(True)
        # plt.show()

        # Сохраняем второй график в байтовый объект
        bytes_io2 = io.BytesIO()
        plt.savefig(bytes_io2, format='png', dpi=300)
        bytes_io2.seek(0)
        fig2_bytes = bytes_io2.getvalue()

        plt.close(fig2)  # Закрываем второй график

        return fig1_bytes, fig2_bytes
    else:
        print("Нет данных для построения графика.")
        return None, None


if __name__ == "__main__":
    # получить список курсов по всем валютам и по всем диапазонам (основная функция (main)) - не нужно её принтить
    full_currencies = get_currencies_mir()
    # получить список доступных валют и дат
    # all_valutes = get_valutes_mir(main=full_currencies)
    all_valutes = get_valutes_mir()
    # получить по конкретной валюте (курс рубля к валюте) за определённую дату
    # получить по конкретной валюте (курс валюты к рублю) за определённую дату
    course = get_course_on_date_mir(main=full_currencies, valute="Кубинский песо", date="16.06.2023")
    # получить график за указанный диапазон (2 графика в PNG, сохранённом в байтовом представлении - рубль к валюте и валюта к рублю)
    charts = draw_currency_chart_mir(main=full_currencies, valute="Казахстанский тенге", start_date="24.02.2022", end_date="16.06.2023")
    # print(charts[0])
    # print(charts[1])


    # калькулятор валюты - пишешь сумму - пишет сколько это число в валюте и в рублях
    # создать задачу на оповещение, если курс станет выше/ниже заданного порогового значения по выбранной валюте
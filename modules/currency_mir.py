from datetime import datetime
import io
import ssl
import requests
import urllib.request

from bs4 import BeautifulSoup as bs
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pdfplumber


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
    target_table_index = 1  # Индекс искомой таблицы (если она вторая, индекс будет 1)
    combined_table = []

    with pdfplumber.open(pdf_file_obj) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()

            if len(tables) > target_table_index:
                # Выбираем нужную таблицу
                target_table = tables[target_table_index]
                combined_table.extend(target_table)

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
        # проверка того чтобы в списке row_data было 5 элементов
        if len(row_data) == 5:
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
    return formatted_data


def get_valutes_mir(main):
    url = "https://mironline.ru/support/list/kursy_mir/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
    }
    soup = bs(requests.get(url=url, headers=headers).content, "lxml")
    valutes = []

    rows = soup.find("table").find_all("tr")
    print(rows)
    for row in rows:
        valute_elem = row.find("p")
        if valute_elem and valute_elem.text.strip() != "Валюта":  # Проверяем наличие элемента и что текст не является пустой строкой и не "Валюта"
            valute = valute_elem.text.strip()
            valutes.append(valute)

    valutes_text = '\n'.join(valutes)

    first_date = main[0]["Date"]
    last_date = main[-1]["Date"]

    result = f"<b>Доступные валюты:</b>\n{valutes_text}\n\n<b>Диапазон дат, за которые имеются данные:</b>\n{last_date} - {first_date}"

    return result


def get_course_today_mir(main, valute):
    valute = valute.capitalize()
    results = []

    for index, data in enumerate(main):
        current_date = main[index]["Date"] if index < len(main) else None
        if valute == data["Valute"] and current_date == data["Date"]:
            currency = float(data["Currency"].replace(",", "."))
            time = data["Time"]
            result = f"""<b>💰 Сегодняшний курс равен курсу за {current_date} {time}</b>

RUB к {valute}: {round(1/currency, 4)}
{valute} к RUB: {currency}
"""
            results.append(result)
            break

    if results:
        return "\n".join(results)
    else:
        return "Некоррктно указана валюта. Воспользуйтесь справкой и попробуйте снова"


def get_course_on_date_mir(main, valute, date):
    valute = valute.capitalize()
    date = date

    results = []

    for data in main:
        if valute == data["Valute"] and date == data["Date"]:
            currency = float(data["Currency"].replace(",", "."))
            time = data["Time"]
            result = f"""<b>💰 Курс за {date} {time}</b>

RUB к {valute}: {round(1/currency, 4)}
{valute} к RUB: {currency}
"""
            results.append(result)

    if results:
        return "\n".join(results)  # Возвращаем все результаты, объединенные символом новой строки
    else:
        return f"За выбранную дату нет данных, либо валюта указана некорректно. Наименования валют перечислены в справке. Если же валюта указана верно, попробуйте другую дату — возможно за сегодня курс не менялся"


def draw_currency_chart_mir(main, valute, start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, "%d.%m.%Y")
        end_date = datetime.strptime(end_date, "%d.%m.%Y")

        dates = []
        rates = []
        rates_rub = []

        for data in main:
            date_str = data["Date"] + " " + data["Time"]  # объединяем дату и время в одну строку
            date = datetime.strptime(date_str, "%d.%m.%Y %H:%M")  # преобразуем строку в объект datetime
            if valute == data["Valute"] and start_date <= date <= end_date:
                dates.append(date)
                currency = float(data["Currency"].replace(",", "."))
                currency_rub = 1 / float(data["Currency"].replace(",", "."))

                rates.append(currency)
                rates_rub.append(currency_rub)

        if len(dates) > 0:
            fig1, ax1 = plt.subplots()
            plt.plot(list(reversed(dates)), list(reversed(rates_rub)), marker='o')
            plt.xlabel("Дата")
            plt.ylabel(valute)
            plt.title(f"Курс рубля к {valute}")
            plt.xticks(rotation=45)
            plt.grid(True)

            # Форматирование даты и времени на шкале x
            date_formatter = mdates.DateFormatter("%d.%m.%Y")
            ax1.xaxis.set_major_formatter(date_formatter)

            for i in range(len(dates)):
                value = round(rates_rub[i], 4)
                ax1.annotate(str(value), xy=(dates[i], rates_rub[i]), xytext=(0, 5), textcoords='offset points')

            # Настройка отступов и расположения элементов
            plt.tight_layout()

            bytes_io1 = io.BytesIO()
            plt.savefig(bytes_io1, format='png', dpi=300)
            bytes_io1.seek(0)
            fig1_bytes = bytes_io1.getvalue()

            plt.close(fig1)

            fig2, ax2 = plt.subplots()
            plt.plot(list(reversed(dates)), list(reversed(rates)), marker='o')
            plt.xlabel("Дата")
            plt.ylabel("Рублей")
            plt.title(f"Курс {valute} к рублю")
            plt.xticks(rotation=45)
            plt.grid(True)

            # Форматирование даты и времени на шкале x
            ax2.xaxis.set_major_formatter(date_formatter)

            for i in range(len(dates)):
                value = round(rates[i], 4)
                ax2.annotate(str(value), xy=(dates[i], rates[i]), xytext=(0, 5), textcoords='offset points')

            # Настройка отступов и расположения элементов
            plt.tight_layout()

            bytes_io2 = io.BytesIO()
            plt.savefig(bytes_io2, format='png', dpi=300)
            bytes_io2.seek(0)
            fig2_bytes = bytes_io2.getvalue()

            plt.close(fig2)

            return fig1_bytes, fig2_bytes
        else:
            return None, None
    except Exception as ex:
        return ex


# if __name__ == "__main__":
    # # Получить список курсов по всем валютам и по всем диапазонам (основная функция)
    # full_currencies = get_currencies_mir()
    
    # # Справка - Получить список доступных валют и дат
    # all_valutes = get_valutes_mir(main=full_currencies)
    
    # # Получить курс по конкретной валюте за сегодня
    # today_course = get_course_today_mir(main=full_currencies, valute="казахстанский тенге")

    # # Получить курс по конкретной валюте за определённую дату
    # course = get_course_on_date_mir(main=full_currencies, valute="казахстанский тенге", date="20.06.2023")

    # # Получить график за указанный диапазон (2 графика в PNG, сохранённом в байтовом представлении - рубль к валюте и валюта к рублю)
    # charts = draw_currency_chart_mir(main=full_currencies, valute="Казахстанский тенге", start_date="01.01.2022", end_date="05.07.2023")
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.common import cb
from keyboards.currency_mir import mir_currency_ikb
from modules.currency_mir import get_valutes_mir, get_currencies_mir, get_course_today_mir, get_course_on_date_mir, draw_currency_chart_mir
from states.common import ProfileStatesGroup
import io


# Справка курса валют для МИР
async def currency_help_mir(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    popup_text = "Минутку, собираю данные для справки"
    await callback.answer(text=popup_text)
    await callback.message.answer(text=get_valutes_mir(get_currencies_mir()), reply_markup=mir_currency_ikb(), parse_mode='html')

# Callback handler для того чтобы попасть в пункт меню "Курс за сегодня"
async def cb_today_currency_mir(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text = """<b>Курс за сегодня.</b>

Напишите название валюты (например, <code>Казахстанский тенге</code>). 
Полный перечень наименования валют можете посмотреть в справке ⬇️
"""
    await ProfileStatesGroup.currency_mir_today_state.set()
    await callback.message.answer(text=text, reply_markup=mir_currency_ikb(), parse_mode='html')

# Message handler - пункт меню "Курс за сегодня"
async def today_currency_mir(message: types.Message):
    popup_text = "Минутку, собираю данные для курса валют..."
    await message.answer(text=popup_text)
    await message.answer(text=get_course_today_mir(main=get_currencies_mir(), valute=message.text), reply_markup=mir_currency_ikb(), parse_mode='html')

# Callback handler для того чтобы попасть в пункт меню "Курс за конкретную дату"
async def cb_currentdate_currency_mir(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text = """<b>Курс за конкретную дату.</b>

Напишите название валюты и дату (например, <code>Казахстанский тенге 05.07.2023</code>). 
Полный перечень наименования валют можете посмотреть в справке ⬇️
"""
    await ProfileStatesGroup.currency_mir_currentdate_state.set()
    await callback.message.answer(text=text, reply_markup=mir_currency_ikb(), parse_mode='html')

# Message handler - пункт меню "Курс за конкретную дату"
async def currentdate_currency_mir(message: types.Message):
    popup_text = "Минутку, собираю данные для курса валют..."
    
    text_parts = message.text.split()
    # Проверка, что текст содержит необходимое количество составляющих (valute и date)
    if len(text_parts) == 3:
        # Valute и date из текста сообщения пользователя
        valute = ' '.join(text_parts[:2])
        date = text_parts[-1]
        
        await message.answer(text=popup_text)
        await message.answer(text=get_course_on_date_mir(main=get_currencies_mir(), valute=valute, date=date), reply_markup=mir_currency_ikb(), parse_mode='html')
    else:
        wrong_text = """<b>Некорректно введены данные. Просьба соблюдать формат.</b>

Напишите название валюты и дату (например, <code>Казахстанский тенге 05.07.2023</code>). 
Полный перечень наименования валют можете посмотреть в справке ⬇️
"""
        await message.answer(text=wrong_text, reply_markup=mir_currency_ikb(), parse_mode='html')

# Callback handler для того чтобы попасть в пункт меню "График за диапазон дат"
async def cb_chart_mir(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text = """<b>График за диапазон дат.</b>

Напишите название валюты и диапазон дат (например, <code>Казахстанский тенге 20.06.2023 05.07.2023</code>). 
Полный перечень наименования валют и диапазона дат можете посмотреть в справке ⬇️
"""
    await ProfileStatesGroup.currency_mir_chart_state.set()
    await callback.message.answer(text=text, reply_markup=mir_currency_ikb(), parse_mode='html')

# Message handler - пункт меню "График за диапазон дат"
async def chart_mir(message: types.Message):
    popup_text = "Минутку, собираю данные для курса валют..."
    await message.answer(text=popup_text)

    try:
        main = get_currencies_mir()
        
        text_parts = message.text.split()
        valute = ' '.join(text_parts[:2])
        start_date = text_parts[-2]
        end_date = text_parts[-1]

        fig1_bytes, fig2_bytes = draw_currency_chart_mir(main=main, valute=valute, start_date=start_date, end_date=end_date)

        if fig1_bytes and fig2_bytes:
            fig1_io = io.BytesIO(fig1_bytes)
            fig2_io = io.BytesIO(fig2_bytes)

            fig1_photo = types.InputFile(fig1_io, filename='chart1.png')
            fig2_photo = types.InputFile(fig2_io, filename='chart2.png')

            await message.answer_photo(fig1_photo, caption=f"График 1 - Курс рубля к {valute}")
            await message.answer_photo(fig2_photo, caption=f"График 2 - Курс {valute} к рублю")
            await message.answer(text="<b>Курсы МИР</b> 🌍", parse_mode="HTML", reply_markup=mir_currency_ikb())

        else:
            error_message = "Нет данных для построения графика."
            await message.answer(text=error_message)
    except Exception:
        await message.answer(
            text=(
                '<b>Некорректно введены данные. Просьба соблюдать формат.</b>'
                '\n\n'
                'Напишите название валюты и диапазон дат'
                '(например, <code>Казахстанский тенге 20.06.2023 05.07.2023</code>).'
                '\n'
                'Полный перечень наименования валют можете посмотреть в справке ⬇️'
            ),
            reply_markup=mir_currency_ikb(),
            parse_mode='html',
        )


# РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ
def register_handlers_currency_mir(dp):
    # Справка
    dp.register_callback_query_handler(currency_help_mir, cb.filter(command='cb_currency_help_mir'), state='*')

    # Курс за сегодня
    dp.register_callback_query_handler(cb_today_currency_mir, cb.filter(command='cb_today_currency_mir'), state='*')
    dp.register_message_handler(today_currency_mir, state=ProfileStatesGroup.currency_mir_today_state)

    # Курс за конкретную дату
    dp.register_callback_query_handler(cb_currentdate_currency_mir, cb.filter(command='cb_currentdate_currency_mir'), state='*')
    dp.register_message_handler(currentdate_currency_mir, state=ProfileStatesGroup.currency_mir_currentdate_state)

    # График за диапазон
    dp.register_callback_query_handler(cb_chart_mir, cb.filter(command='cb_chart_mir'), state='*')
    dp.register_message_handler(chart_mir, state=ProfileStatesGroup.currency_mir_chart_state)

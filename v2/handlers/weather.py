from aiogram import types
from aiogram.dispatcher import FSMContext
from create_bot import dp
from keyboards.common import cb, cancel_ikb
from keyboards.weather import weather_ikb
from modules.weather import get_weather, get_forecast_weather
from states.common import ProfileStatesGroup
from aiogram.utils.exceptions import MessageIsTooLong
from config import OPEN_WEATHER_TOKEN


# Погода
@dp.callback_query_handler(cb.filter(command='weather'), state='*')
async def cb_weather(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await ProfileStatesGroup.weather.set()
    await callback.message.edit_text("Выберите необходимый период", reply_markup=weather_ikb())

# Текущая погода и 3-х часовые интервалы
@dp.callback_query_handler(cb.filter(), state=ProfileStatesGroup.weather)
async def cb_current_weather(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['command'] == 'weather_current':
        await ProfileStatesGroup.current_weather.set()
        await callback.message.edit_text("Напишите название города", reply_markup=cancel_ikb())
    elif callback_data['command'] == 'forecast_weather':
        await ProfileStatesGroup.forecast_weather.set()
        await callback.message.edit_text("Укажите название города и количество 3-часовых интервалов (до 40), разделив их пробелом. В случае, если интервал не указан явно, применяется значение по умолчанию — 2 интервала.", reply_markup=cancel_ikb())

# Вызов модуля текущей погоды
@dp.message_handler(state=ProfileStatesGroup.current_weather)
async def current_weather(message: types.Message):
    await message.answer(text=get_weather(message.text, OPEN_WEATHER_TOKEN), reply_markup=cancel_ikb(), parse_mode='html')


# Вызов модуля прогноза погоды
@dp.message_handler(state=ProfileStatesGroup.forecast_weather)
async def forecast_weather(message: types.Message):
    # если есть число, подставляем в количество итераций по 3 часа, если нет то по умолчанию 1 итерация
    text_part = message.text.strip().split()
    if text_part[-1].isdigit():
        hours_count = int(text_part[-1])
    else:
        hours_count = 2

    # если последнее слово это число, то оно убирается
    if text_part[-1].isdigit():
        city = ' '.join(text_part[:-1])
    else:
        city = message.text
    
    text = get_forecast_weather(city, OPEN_WEATHER_TOKEN, count=hours_count)
    MAX_MESSAGE_LENGTH = 4096
    chunks = [text[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]
    for chunk in chunks:
        try:
            await message.answer(text=chunk, reply_markup=cancel_ikb(), parse_mode='html')
        except MessageIsTooLong:
            continue
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.common import cb

def weather_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Текущая погода ☀️", callback_data=cb.new('weather_current')),
         InlineKeyboardButton(text="Интервал в 3 часа 🌤", callback_data=cb.new('forecast_weather'))],
        [InlineKeyboardButton(text="Вернуться в главное меню ⬅️", callback_data=cb.new('cancel'))]
])
    return ikb

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.common import cb

# Клавиатура Курса Валют МИР
def mir_currency_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Справка ❓", callback_data=cb.new('cb_currency_help_mir'))],
        [InlineKeyboardButton(text="Курс за сегодня 💱", callback_data=cb.new('cb_today_currency_mir'))],
        [InlineKeyboardButton(text="Курс за конкретную дату 📆", callback_data=cb.new('cb_currentdate_currency_mir'))],
        [InlineKeyboardButton(text="График за диапазон дат 🗓", callback_data=cb.new('cb_chart_mir'))],
        [InlineKeyboardButton(text="Вернуться в главное меню ⬅️", callback_data=cb.new('cancel'))]
])
    return ikb

# Клавиатура справка и назад
def mir_currency_cancel_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Справка ❓", callback_data=cb.new('cb_currency_help_mir'))],
        [InlineKeyboardButton(text="Вернуться в главное меню ⬅️", callback_data=cb.new('cancel'))]
])
    return ikb

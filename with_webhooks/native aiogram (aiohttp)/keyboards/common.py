from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cb = CallbackData('ikb', 'command')

# Главное меню
def main_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Погода ☀️", callback_data=cb.new('weather'))],
        [InlineKeyboardButton(text="Курсы валют 💰", callback_data=cb.new('currency'))],
        [InlineKeyboardButton(text="Посмотреть котика 😺", callback_data=cb.new('cat'))]
])
    return ikb

# Отмена для возврата в главное меню
def cancel_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в главное меню 📝", callback_data=cb.new('cancel'))]
])
    return ikb

# Выбор курса ЦБ РФ/МИР
def choose_currency() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ЦБ РФ 🏦", callback_data=cb.new('cb_currency_cbrf')),
        InlineKeyboardButton(text="МИР 🌍", callback_data=cb.new('cb_currency_mir'))],
        [InlineKeyboardButton(text="Вернуться в главное меню 📝", callback_data=cb.new('cancel'))]
])
    return ikb
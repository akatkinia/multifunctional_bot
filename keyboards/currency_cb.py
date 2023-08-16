from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.common import cb


# Клавиатура Курса Валют ЦБ РФ
def currency_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Справка ❓", callback_data=cb.new('currency_help'))],
        [InlineKeyboardButton(text="Вернуться в главное меню ⬅️", callback_data=cb.new('cancel'))]
])
    return ikb

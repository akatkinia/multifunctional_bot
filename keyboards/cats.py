from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.common import cb


def cat_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Фото котика 😼", callback_data=cb.new('cat_photo'))],
        [InlineKeyboardButton(text="Вернуться в главное меню ⬅️", callback_data=cb.new('cancel'))]
])
    return ikb

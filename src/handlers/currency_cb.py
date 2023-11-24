from aiogram import types
from aiogram.dispatcher import FSMContext

from create_bot import dp
from keyboards.currency_cb import currency_ikb
from keyboards.common import cb, cancel_ikb
from modules.currency_cb import get_valutes, get_course
from states.common import ProfileStatesGroup


# Справка курса валют для ЦБ РФ
async def cb_currency_help(callback: types.CallbackQuery, callback_data: dict, state : FSMContext):
    await callback.message.answer(text=get_valutes(), reply_markup=cancel_ikb(), parse_mode='html')

# Вызов курса валют
async def currency(message: types.Message):
    await message.answer(text=get_course(message.text), reply_markup=currency_ikb(), parse_mode='html')


# РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ
def register_handlers_currency_cb(dp: dp):
    dp.register_callback_query_handler(cb_currency_help, cb.filter(command='currency_help'), state=ProfileStatesGroup.currency)
    dp.register_message_handler(currency, state=ProfileStatesGroup.currency)
    
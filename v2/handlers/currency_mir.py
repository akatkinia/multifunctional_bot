from aiogram import types
from aiogram.dispatcher import FSMContext
from create_bot import dp
from keyboards.common import cb, cancel_ikb
from modules.currency_mir import get_valutes_mir, get_currencies_mir
from states.common import ProfileStatesGroup


########## Обработчики для МИР #################
# Справка курса валют для МИР
# @dp.callback_query_handler(cb.filter(command='cb_currency_help_mir'), state=ProfileStatesGroup.currency_mir)
async def currency_help_mir(callback: types.CallbackQuery, callback_data: dict, state : FSMContext):
    popup_text = "Минутку, собираю данные для справки"
    # if callback_data['command'] == 'cb_currency_help_mir':
    await callback.answer(text=popup_text)
    await callback.message.answer(text=get_valutes_mir(get_currencies_mir()), reply_markup=cancel_ikb(), parse_mode='html')
    await callback.message.delete()

def register_handlers_currency_mir(dp: dp):
    dp.register_callback_query_handler(currency_help_mir, cb.filter(command='cb_currency_help_mir'), state=ProfileStatesGroup.currency_mir)



# dp.register_callback_query_handler(
#     cb_currency_help_mir,
#     lambda callback_query: cb.filter(command='cb_currency_help_mir')(callback_query) and
#                           ProfileStatesGroup.currency_mir(callback_query.message.chat.id)
# )

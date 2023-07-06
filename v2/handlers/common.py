from aiogram import types
from aiogram.dispatcher import FSMContext
from create_bot import dp
from keyboards.common import cb, main_ikb, choose_currency
from keyboards.currency_cb import currency_ikb
from keyboards.currency_mir import mir_currency_ikb
from states.common import ProfileStatesGroup
from aiogram.dispatcher.filters import Command

# Обработка команд 'start' и cancel
# @dp.message_handler(commands=['start', 'cancel'], state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=f"Добро пожаловать, {message.from_user.full_name}!",
                         reply_markup=main_ikb())
    await message.delete()

# Обработка callback 'cancel' для всех состояний
# @dp.callback_query_handler(cb.filter(command='cancel'), state='*')
async def cb_cancel(callback: types.CallbackQuery, state: FSMContext):
    # если состояние FSM является котиком, то вернуть в виде ответа, в остальных случаях редактированием текста
    hello_text = "Добро пожаловать! Снова."
    if await state.get_state() == "ProfileStatesGroup:cat":
        await state.finish()
        await callback.message.answer(text=hello_text, reply_markup=main_ikb())
        await callback.message.delete()
    else:
        await state.finish()
        await callback.message.edit_text(text=hello_text, reply_markup=main_ikb())

# Курсы валют
# @dp.callback_query_handler(cb.filter(command='currency'), state='*')
async def cb_currency(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    # await ProfileStatesGroup.currency.set()
    await callback.message.edit_text("Выберите источник", reply_markup=choose_currency())

#Выбор ЦБ РФ
# @dp.callback_query_handler(cb.filter(command='cb_currency_cbrf'), state='*')
async def cb_currency_cbrf(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    # if callback_data['command'] == 'cb_currency_cbrf':
    await ProfileStatesGroup.currency.set()
    await callback.message.edit_text("Напишите мнемокод валюты, курс которой хотите узнать (например <code>USD</code>). Для получения списка мнемокодов, вызовите справку ⬇️", parse_mode="HTML", reply_markup=currency_ikb())

#Выбор МИР
# @dp.callback_query_handler(cb.filter(command='cb_currency_mir'), state='*')
async def cb_mir_currency(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['command'] == 'cb_currency_mir':
        # await ProfileStatesGroup.currency_mir_state.set()
        await callback.message.edit_text(f"Выберите способ отображения данных.\nЕсли требуется информация о доступных на сегодняшний день валютах и диапазонах дат, вызовите справку ⬇️", parse_mode="HTML", reply_markup=mir_currency_ikb())


# команды для регистрации handlers для бота - они передаются в основной файл bot.py
def register_handlers_common(dp: dp):
    dp.register_message_handler(cmd_start, commands=['start', 'cancel'], state='*')
    dp.register_callback_query_handler(cb_cancel, cb.filter(command='cancel'), state='*')
    dp.register_callback_query_handler(cb_currency, cb.filter(command='currency'), state='*')
    dp.register_callback_query_handler(cb_currency_cbrf, cb.filter(command='cb_currency_cbrf'), state='*')
    dp.register_callback_query_handler(cb_mir_currency, cb.filter(command='cb_currency_mir'), state='*')
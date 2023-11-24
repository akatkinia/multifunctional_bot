from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.common import cb, choose_currency, main_ikb
from keyboards.currency_cb import currency_ikb
from keyboards.currency_mir import mir_currency_ikb
from states.common import ProfileStatesGroup


# Обработка команд start и cancel
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=f"Добро пожаловать, {message.from_user.full_name}!",
                         reply_markup=main_ikb())
    await message.delete()

# Обработка callback 'cancel' для всех состояний
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
async def cb_currency(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.message.edit_text("Выберите источник", reply_markup=choose_currency())

# Выбор ЦБ РФ
async def cb_currency_cbrf(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await ProfileStatesGroup.currency.set()
    await callback.message.edit_text("Напишите мнемокод валюты, курс которой хотите узнать (например <code>USD</code>). Для получения списка мнемокодов, вызовите справку ⬇️", parse_mode="HTML", reply_markup=currency_ikb())

# Выбор МИР
async def cb_mir_currency(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['command'] == 'cb_currency_mir':
        await callback.message.edit_text(f"Выберите способ отображения данных.\nЕсли требуется информация о доступных на сегодняшний день валютах и диапазонах дат, вызовите справку ⬇️", parse_mode="HTML", reply_markup=mir_currency_ikb())


# РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ
def register_handlers_common(dp):
    dp.register_message_handler(cmd_start, commands=['start', 'cancel'], state='*')
    dp.register_callback_query_handler(cb_cancel, cb.filter(command='cancel'), state='*')
    dp.register_callback_query_handler(cb_currency, cb.filter(command='currency'), state='*')
    dp.register_callback_query_handler(cb_currency_cbrf, cb.filter(command='cb_currency_cbrf'), state='*')
    dp.register_callback_query_handler(cb_mir_currency, cb.filter(command='cb_currency_mir'), state='*')

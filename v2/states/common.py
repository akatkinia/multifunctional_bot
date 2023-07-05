from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileStatesGroup(StatesGroup):
    weather = State()
    current_weather = State()
    forecast_weather = State()
    # состояние cat используется только для корректной работы callback обработчика cancel
    cat = State()

    currency = State()
    currency_mir = State()
    # currency_help = State()
    currency_current = State()
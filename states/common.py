from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileStatesGroup(StatesGroup):
    ### Погода ###
    weather = State()
    current_weather = State()
    forecast_weather = State()

    ### Коты ###
    cat = State()

    ### Курсы ЦБ ###
    currency = State()
    currency_current = State()

    ### Курсы МИР ###
    currency_mir_state = State() # состояние для меню курса валют МИР
    currency_mir_today_state = State() # состояние для пункта "Курс за сегодня"
    currency_mir_currentdate_state = State() # состояние для пункта "Курс за конкретную дату"
    currency_mir_chart_state = State() # состояние для пункта "График за диапазон дат"

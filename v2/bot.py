from aiogram import executor
from create_bot import dp
from handlers import common, cats, currency_cb, currency_mir, weather

if __name__ == '__main__':
    weather.register_handlers_weather(dp)
    common.register_handlers_common(dp)

    currency_cb.register_handlers_currency_cb(dp)
    currency_mir.register_handlers_currency_mir(dp)
    cats.register_handlers_cats(dp)


    executor.start_polling(dispatcher=dp, skip_updates=True)
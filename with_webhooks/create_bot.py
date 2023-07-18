# import logging
from aiogram import Dispatcher, Bot
from config import TOKEN_API
from config import WEBHOOK_URL, WEBHOOK_PATH
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from fastapi import FastAPI
from aiogram import types


storage = MemoryStorage()

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot=bot, storage=storage)

# logging.basicConfig(level=logging.INFO)
# dp.middleware.setup(LoggingMiddleware())

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )

@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    dp.skip_updates = True
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)

@app.on_event("shutdown")
async def on_shutdown():
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()
    # Закрываем соединение с базой данных (если используется)
    await dp.storage.close()
    await dp.storage.wait_closed()

    session = await bot.get_session()
    await session.close()


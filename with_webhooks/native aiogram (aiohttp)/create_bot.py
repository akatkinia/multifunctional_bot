import logging

from aiogram import Dispatcher, Bot, types
from config import TOKEN_API
from config import WEBHOOK_URL
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware

storage = MemoryStorage()

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot=bot, storage=storage)

# logging.basicConfig(level=logging.INFO)
# добавляем middleware on_pre_process_message перед другими обработчиками message_handler для захвата сообщений пользователя
class LoggingMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        username = message.from_user.username
        text = message.text
        logging.info(f"Received message from user {user_id} (@{username}): {text}")

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        user_id = callback_query.from_user.id
        username = callback_query.from_user.username
        data = callback_query.data
        logging.info(f"Received callback query from user {user_id} (@{username}): {data}")    

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', encoding='utf-8')
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown
    await dp.storage.close()
    await dp.storage.wait_closed()
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()
    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    session = await bot.get_session()
    await session.close()

    logging.warning('Bye!')

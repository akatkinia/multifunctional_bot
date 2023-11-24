import logging
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.middlewares import BaseMiddleware
from datetime import datetime
import sqlite3

from config import ADMIN_ID, DB_PATH, TOKEN_API, WEBHOOK_URL
from db import create_table


class LoggingMiddleware(BaseMiddleware):
    # Middleware для захвата сообщений пользователя перед другими обработчиками message_handler - запись в БД и лог-файл
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        nickname = message.from_user.username
        username = message.from_user.full_name
        text = message.text
        current_date_time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S-%f')

        if message.photo:
            text = message.caption

            # Если его нет, создаем подкаталог persistant_data/photos/
            save_photo_dir = os.path.join('users_data', 'photos')
            # Определяем название файла в формате "{user_id}_{current_date_time}.jpg"
            save_photo_path = os.path.join(save_photo_dir, f"{user_id}_{current_date_time}.jpg")
            # Скачиваем фото
            await message.photo[-1].download(destination_file=save_photo_path)

        logging.info(f"Received message from user {user_id} (@{nickname}): {text}")

        # Запись действия пользователя в БД users_messages
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users_messages (date, user_id, username, nickname, message, photo, sticker) VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (current_date_time, user_id, username, nickname, text if text else None,
                            save_photo_path if message.photo else None,
                            message.sticker.file_id if message.sticker else None))
            conn.commit()
        except Exception as ex:
            logging.error(f"Exception: {ex}")    
        finally:
            cursor.close()

    # Middleware для захвата callback queries от пользователя - запись в лог-файл
    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        user_id = callback_query.from_user.id
        username = callback_query.from_user.username
        data = callback_query.data
        logging.info(f"Received callback query from user {user_id} (@{username}): {data}")    


def bot_create():
    storage = MemoryStorage()

    bot = Bot(token=TOKEN_API)
    dp = Dispatcher(bot=bot, storage=storage)

    logging.basicConfig(filename='./persistant_data/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', encoding='utf-8')
    dp.middleware.setup(LoggingMiddleware())
    return dp


async def on_startup(dp):
    await dp.bot.set_webhook(WEBHOOK_URL)
    # Создание таблицы
    create_table()
    # создание постоянного соединения с БД при запуске бота
    global conn
    conn = sqlite3.connect(DB_PATH)
    await dp.bot.send_message(chat_id=ADMIN_ID, text=f'Mixer bot is online')


async def on_shutdown(dp):
    logging.warning('Shutting down...')
    await dp.bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    session = await dp.bot.get_session()
    await session.close()
    # закрытия соединения с БД при завершении работы бота
    conn.close()
    await dp.bot.send_message(chat_id=ADMIN_ID, text=f'Mixer bot is offline')
    logging.warning('Bye!')

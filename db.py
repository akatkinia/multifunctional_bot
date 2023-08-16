import sqlite3
from config import DB_PATH


def create_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_messages (
                date TEXT,
                user_id INTEGER,
                username TEXT,
                nickname TEXT,
                message TEXT,
                photo TEXT,
                sticker TEXT
            )
        ''')

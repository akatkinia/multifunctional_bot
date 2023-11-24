# Telegram
TOKEN_API = '' # Ваш Telegram API токен

# OpenWeather
OPEN_WEATHER_TOKEN = '' # Ваш Open Weather токен

# DB
DB_PATH = './persistant_data/mixer_bot_prod.db'

# Настройки оповещений
ADMIN_ID = '' # укажите ваш id. Работает для оповещения администратора о работе бота (старт/завершение работы)

# Webhook settings
WEBAPP_HOST = '0.0.0.0'  # public dns/ip or 0.0.0.0
WEBAPP_PORT = 8443 # aiogram работает с 80, 88, 443, 8443
DOMAIN_NAME = '' # укажите ваше доменное имя сервера, на котором запускается бот
WEBHOOK_HOST = f'{DOMAIN_NAME}:{WEBAPP_PORT}'
WEBHOOK_PATH = f'/bot{TOKEN_API}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBHOOK_SSL_CERT = './persistant_data/certs/fullchain.pem'  # разметстите здесь ваш сертификат
WEBHOOK_SSL_PRIV = './persistant_data/certs/privkey.pem'  # разместите здесь приватный ключ сертификата

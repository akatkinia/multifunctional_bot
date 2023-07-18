from create_bot import dp, on_startup, on_shutdown
from handlers import common, cats, currency_cb, currency_mir, weather
from config import WEBAPP_PORT, WEBAPP_HOST, WEBHOOK_PATH
from aiogram.utils.executor import start_webhook
from config import WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV
import ssl


if __name__ == '__main__':
    # Generate SSL context
   # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2) # deprecated
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)


    weather.register_handlers_weather(dp)
    common.register_handlers_common(dp)
    currency_cb.register_handlers_currency_cb(dp)
    currency_mir.register_handlers_currency_mir(dp)
    cats.register_handlers_cats(dp)

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        ssl_context=context
    )

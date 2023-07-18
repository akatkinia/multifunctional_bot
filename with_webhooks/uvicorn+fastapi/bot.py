from create_bot import dp
from handlers import common, cats, currency_cb, currency_mir, weather
from config import WEBAPP_PORT

import uvicorn
from create_bot import app

if __name__ == '__main__':
    weather.register_handlers_weather(dp)
    common.register_handlers_common(dp)
    currency_cb.register_handlers_currency_cb(dp)
    currency_mir.register_handlers_currency_mir(dp)
    cats.register_handlers_cats(dp)

#    uvicorn.run(app, host='0.0.0.0', port=WEBAPP_PORT, ssl_keyfile='cert/key.pem', ssl_certfile='cert/cert.pem')
    uvicorn.run(app, host='0.0.0.0', port=WEBAPP_PORT, ssl_keyfile='/etc/letsencrypt/live/<DNS_OF_YOUR_HOST>/privkey.pem', ssl_certfile='/etc/letsencrypt/live/<DNS_OF_YOUR_HOST>/fullchain.pem')

#    uvicorn.run(app, host='0.0.0.0', port=WEBAPP_PORT)

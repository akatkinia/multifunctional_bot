#telegram
#Test
# TOKEN_API = ''
#Prod
TOKEN_API = ''
# https://api.telegram.org/bot<TOKEN_API>/getWebhookInfo
# https://api.telegram.org/<TOKEN_API>/setWebhook?url=<WEBHOOK_HOST>
# https://api.telegram.org/bot<TOKEN_API>/deletewebhook


# ADMIN_ID = ""

# webhook settings
WEBAPP_PORT = 8443
WEBHOOK_HOST = f'https://<DNS_OF_YOUR_HOST>:{WEBAPP_PORT}'
WEBHOOK_PATH = f'/bot{TOKEN_API}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

#openweather
OPEN_WEATHER_TOKEN = ''

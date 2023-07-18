#telegram
TOKEN_API = ''
# ADMIN_ID = ''

# webhook settings
WEBAPP_HOST = '<PUBLIC_IP_OF_YOUR_HOST>'  # public dns/ip or 0.0.0.0
WEBAPP_PORT = 8443 # 443 or 8443

WEBHOOK_HOST = f'<DNS_OF_YOUR_HOST>:{WEBAPP_PORT}'
WEBHOOK_PATH = f'/bot{TOKEN_API}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBHOOK_SSL_CERT = '/etc/letsencrypt/live/<DNS_OF_YOUR_HOST>/fullchain.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '/etc/letsencrypt/live/<DNS_OF_YOUR_HOST>/privkey.pem'  # Path to the ssl private key

#openweather
OPEN_WEATHER_TOKEN = ''

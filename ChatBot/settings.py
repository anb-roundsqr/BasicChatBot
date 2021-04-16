from .settings_base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '3.19.220.112', 'api.chatbotdev.roundsqr.net']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'http://app.chatbotdev.roundsqr.net',
    'http://localhost:3000',
)


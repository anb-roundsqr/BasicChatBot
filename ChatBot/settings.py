from .settings_base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

FRONTEND_URL = "https://app.chatbotdev.roundsqr.net"
BACKEND_URL = "https://api.chatbotdev.roundsqr.net"
CLIENT_URL = "http://chat-bot-client.s3-website-ap-southeast-2.amazonaws.com"

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '3.19.220.112', 'api.chatbotdev.roundsqr.net']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    FRONTEND_URL,
    'http://localhost:3000',
)

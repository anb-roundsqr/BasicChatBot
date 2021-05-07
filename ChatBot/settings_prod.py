from .settings_base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

FRONTEND_URL = "https://app.chatbot.roundsqr.net"
BACKEND_URL = "https://api.chatbot.roundsqr.net"

ALLOWED_HOSTS = ['3.19.204.159', 'api.chatbot.roundsqr.net']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    FRONTEND_URL,
)

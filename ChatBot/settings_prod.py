from .settings_base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
env.read_env()

FRONTEND_URL = env('FRONTEND_URL')
BACKEND_URL = env('BACKEND_URL')
CLIENT_URL = env('CLIENT_URL')

ALLOWED_HOSTS = env('HOSTS').split(',')

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    FRONTEND_URL,
)

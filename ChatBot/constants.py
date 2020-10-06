import logging

logging.basicConfig(
    filename='test_log.log',
    level=logging.INFO,
    filemode='a',
    format='%(asctime)s %(process)d-%(name)-12s'
           ' %(levelname)-8s -%(funcName)s  -  %(lineno)d     %(message)s'
)

# Get an instance of a logger
logger = logging.getLogger(__name__)

POWER_BOT_WEB_SITE = 'https://www.firstmatch.com/'


EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587

# first match gmail account
EMAIL_HOST_USER = b'Zmlyc3RtYXRjaC5hZGVscGhvaUBnbWFpbC5jb20='
EMAIL_HOST_PASSWORD = b'MUFkM2xwaDAh'

# gmail account
# EMAIL_HOST_USER = b'bmFyYXlhbmExNWFkaUBnbWFpbC5jb20='
# EMAIL_HOST_PASSWORD = b'bHFyenVmbmRidXJ4dmp2dw=='

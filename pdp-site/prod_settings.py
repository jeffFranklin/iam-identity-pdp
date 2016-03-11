import os
from settings import LOGGING

# local additions to settings

DEBUG = False
SECRET_KEY = open(os.path.join('/data/local/etc', 'pdp-secret')).read().strip()
TEMPLATE_DEBUG = False
USER_SERVICE_NO_DEFAULT_USER = True
LOGIN_URL = '/id/login/'
STATIC_URL = '/static-id/'
STATIC_ROOT = 'static-id'

ALLOWED_HOSTS = ['*']
COMPRESS_ENABLED = False

# IRWS settings (dev host)

RESTCLIENTS_IRWS_DAO_CLASS = 'restclients.dao_implementation.irws.Live'
RESTCLIENTS_IRWS_HOST = 'https://mango.u.washington.edu:646'
RESTCLIENTS_IRWS_SERVICE_NAME = 'registry'
RESTCLIENTS_IRWS_CERT_FILE = '/data/local/django/pdp/certs/identity.uw.edu.uwca.cert'
RESTCLIENTS_IRWS_KEY_FILE = '/data/local/django/pdp/certs/identity.uw.edu.uwca.key'
RESTCLIENTS_CA_BUNDLE = '/usr/local/ssl/certs/ca-bundle.crt'
RESTCLIENTS_IRWS_MAX_POOL_SIZE = 10

LOGGING['handlers'].update({
    'debuglog': {
        'level': 'DEBUG',
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'formatter': 'verbose',
        'filename': '/logs/pdp/process.log',
        'when': 'midnight'
    }
})

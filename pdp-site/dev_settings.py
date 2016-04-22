# local additions to settings
import os
from settings import LOGGING

DEBUG = True
SECRET_KEY = open(os.path.join('/data/local/etc', 'pdp-secret')).read().strip()
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']
COMPRESS_ENABLED = True

RESTCLIENTS_IRWS_DAO_CLASS = 'restclients.dao_implementation.irws.Live'
RESTCLIENTS_IRWS_HOST = 'https://mango-dev.u.washington.edu:646'
RESTCLIENTS_IRWS_SERVICE_NAME = 'registry-dev'
# RESTCLIENTS_IRWS_HOST = 'https://mango-eval.u.washington.edu:646'
# RESTCLIENTS_IRWS_SERVICE_NAME = 'registry-eval'

RESTCLIENTS_IRWS_CERT_FILE = '/usr/local/ssl/certs/identity.uw.edu.uwca.cert'
RESTCLIENTS_IRWS_KEY_FILE = '/usr/local/ssl/certs/identity.uw.edu.uwca.key'
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



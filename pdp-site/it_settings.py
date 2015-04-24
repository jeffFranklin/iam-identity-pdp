from settings import *

MIDDLEWARE_CLASSES = tuple(x for x in MIDDLEWARE_CLASSES 
                           if x != 'django.middleware.csrf.CsrfViewMiddleware')

# IRWS settings (dev host)

RESTCLIENTS_IRWS_DAO_CLASS = 'restclients.dao_implementation.irws.Live'

# RESTCLIENTS_IRWS_HOST = 'https://mango-dev.u.washington.edu:646'
# RESTCLIENTS_IRWS_SERVICE_NAME = 'registry-dev'
RESTCLIENTS_IRWS_HOST = 'https://mango-eval.u.washington.edu:646'
RESTCLIENTS_IRWS_SERVICE_NAME = 'registry-eval'

RESTCLIENTS_IRWS_CERT_FILE = 'gofindit'
RESTCLIENTS_IRWS_KEY_FILE = 'gofindit'
RESTCLIENTS_CA_BUNDLE = '/usr/local/ssl/certs/ca-bundle.crt'
RESTCLIENTS_IRWS_MAX_POOL_SIZE = 10

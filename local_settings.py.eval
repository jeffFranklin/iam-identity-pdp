# local additions to settings
import os

DEBUG = True
SECRET_KEY = open(os.path.join('/data/local/etc', 'pdp-secret')).read().strip()
TEMPLATE_DEBUG = True
USER_SERVICE_NO_DEFAULT_USER = True
LOGIN_URL = '/pdp/login/'
STATIC_URL = '/static-pdp/'
ALLOWED_HOSTS = ['*']


RESTCLIENTS_IRWS_CERT_FILE = '/data/local/etc/x315.crt'
RESTCLIENTS_IRWS_KEY_FILE = '/data/local/etc/x315.key'
RESTCLIENTS_CA_BUNDLE = '/data/local/etc/cacerts.cert'
RESTCLIENTS_IRWS_MAX_POOL_SIZE = 10


RESTCLIENTS_IRWS_DAO_CLASS = 'restclients.dao_implementation.irws.Live'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s %(levelname)s '
                       '%(module)s.%(funcName)s():%(lineno)d: '
                       '%(message)s')
            },
        },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'debuglog': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/logs/pdp/process.log',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['debuglog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'pdp': {
            'handlers': ['debuglog'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


"""Settings to be used for integration testing."""
from settings import *

MOCK_LOGIN_CLASS = 'idbase.middleware.MockLoginMiddleware'

if MOCK_LOGIN_CLASS not in MIDDLEWARE_CLASSES:
    MIDDLEWARE_CLASSES = [MOCK_LOGIN_CLASS] + MIDDLEWARE_CLASSES

LOGGING['handlers'].update({
    'debuglog': {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
        'formatter': 'verbose',
        'stream': 'ext://sys.stdout',
    }
})

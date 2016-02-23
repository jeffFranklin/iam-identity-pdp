from dev_settings import *
from settings import MIDDLEWARE_CLASSES

RESTCLIENTS_IRWS_DAO_CLASS = 'restclients.dao_implementation.irws.File'
RESTCLIENTS_IRWS_SERVICE_NAME = 'registry-dev'
LOGIN_URL = '/id/mocklogin'  # Hide the LOGIN_URL from shib
MIDDLEWARE_CLASSES.insert(0, 'idbase.middleware.MockLoginMiddleware')

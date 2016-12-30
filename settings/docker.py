from dev_settings import *
from settings import MIDDLEWARE_CLASSES

RESTCLIENTS_RUN_MODE = 'File'
RESTCLIENTS_IRWS_SERVICE_NAME = 'registry-dev'
LOGIN_URL = '/profile/mocklogin'  # Hide the LOGIN_URL from shib
MIDDLEWARE_CLASSES.insert(0, 'idbase.middleware.MockLoginMiddleware')
MOCK_LOGIN_USER = 'user1e@washington.edu'

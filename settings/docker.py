from .dev import *

ALLOWED_HOSTS = ['docker.internal']
IS_RESTTOOLS_LIVE = False
IRWS_URL = 'https://mango-dev.u.washington.edu:443/registry-dev'
LOGIN_URL = '/profile/mocklogin'  # Hide the LOGIN_URL from shib
MOCK_LOGIN_USER = 'user1e@washington.edu'
USE_MOCK_LOGIN = True

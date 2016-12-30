"""Dev settings that override the base settings."""
from settings import *

DEBUG = True
SECRET_KEY = open(os.path.join('/data/local/etc', 'pdp-secret')).read().strip()
ALLOWED_HOSTS = ['identity-dev.s.uw.edu']
COMPRESS_ENABLED = True
SESSION_COOKIE_SECURE = True

IS_RESTTOOLS_LIVE = True
USE_MOCK_LOGIN = False
MOCK_LOGIN_USER = ''
IRWS_URL = 'https://mango-eval.u.washington.edu:646/registry-eval'

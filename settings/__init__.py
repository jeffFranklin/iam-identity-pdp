import os
from pdp import __version__
from .logging import LOGGING
DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'set-this-externally'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'idbase',
    'pdp'
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'idbase.middleware.session_timeout_middleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'idbase.middleware.mock_login_middleware',
    'idbase.middleware.login_url_middleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware']

ROOT_URLCONF = 'pdp.urls'
WSGI_APPLICATION = 'wsgi.application'

PDP_BASE = '/profile/'
LOGIN_URL = '/profile/login/'
LOGOUT_URL = '/profile/logout/'
PROFILE_URL = '/profile/'
RECOVERY_OPTIONS_URL = '/account/recovery/'
PROFILE_IMPERSONATORS_GROUP = 'u_identity_profile_impersonators'
PUBLISH_PREVIEWERS_GROUP = 'u_identity_profile_publish-previewers'
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_NAME = 'pdpsession'
SESSION_COOKIE_PATH = '/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SETTINGS_CONTEXT_ATTRIBUTES = ['DEBUG', 'LOGOUT_URL', 'PDP_BASE',
                               'PROFILE_URL', 'RECOVERY_OPTIONS_URL']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'idbase.context_processors.settings_context'
            ],
        },
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True
COMPRESS_ENABLED = False
COMPRESS_OUTPUT_DIR = 'cache-' + __version__


STATIC_URL = '/static-profile/' + __version__ + '/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-profile', __version__)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

IS_RESTTOOLS_LIVE = False
IRWS_URL = 'https://mango-dev.u.washington.edu:443/registry-dev'
GWS_URL = 'https://iam-ws.u.washington.edu:7443/gws'
CERT_FILE = '/usr/local/ssl/certs/identity.uw.edu.uwca.cert'
KEY_FILE = '/usr/local/ssl/certs/identity.uw.edu.uwca.key'
CA_FILE = '/usr/local/ssl/certs/ca-bundle.crt'
USE_MOCK_LOGIN = True
MOCK_LOGIN_USER = 'user1e@washington.edu'
IDBASE_IRWS_CLASS = 'pdp.dao.IRWS'

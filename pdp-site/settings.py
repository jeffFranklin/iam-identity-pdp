import os
from pdp import __version__
# Django setting for personal prefs
# These can be reset in 'local_settings.py'
DEBUG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'set-in-local_settings'
ALLOWED_HOSTS = []

# Application definition

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

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'idbase.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'idbase.middleware.LoginUrlMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware']

ROOT_URLCONF = 'pdp-site.urls'

WSGI_APPLICATION = 'pdp-site.wsgi.application'

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


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db/db.sqlite3'),
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
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': 'ext://sys.stdout',
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
        'resttools': {
            'handlers': ['debuglog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'idbase': {
            'handlers': ['debuglog'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True
COMPRESS_ENABLED = False
COMPRESS_OUTPUT_DIR = 'cache-' + __version__


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static-profile/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-profile')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'pdp/static'),
)


# PWS settings
RESTCLIENTS_RUN_MODE = 'File'
RESTCLIENTS_IRWS_HOST = 'https://mango-dev.u.washington.edu:443'
RESTCLIENTS_IRWS_SERVICE_NAME = 'registry-dev'
RESTCLIENTS_IRWS_CERT_FILE = '/data/local/etc/x315.crt'
RESTCLIENTS_IRWS_KEY_FILE = '/data/local/etc/x315.key'
RESTCLIENTS_CA_BUNDLE = '/data/local/etc/cacerts.cert'
RESTCLIENTS_IRWS_MAX_POOL_SIZE = 10
RESTCLIENTS_GWS_HOST = 'https://iam-ws.u.washington.edu:7443'
RESTCLIENTS_GWS_SERVICE = 'gws'
RESTCLIENTS_TIMEOUT = None
MOCK_LOGIN_USER = 'user1e@washington.edu'
IDBASE_IRWS_CLASS = 'pdp.dao.IRWS'
try:
    from local_settings import *
except ImportError:
    pass

SESSION_COOKIE_SECURE = not DEBUG
IRWS_CONF = dict(HOST=RESTCLIENTS_IRWS_HOST,
                 SERVICE_NAME=RESTCLIENTS_IRWS_SERVICE_NAME,
                 CERT_FILE=RESTCLIENTS_IRWS_CERT_FILE,
                 KEY_FILE=RESTCLIENTS_IRWS_KEY_FILE,
                 CA_FILE=RESTCLIENTS_CA_BUNDLE,
                 RUN_MODE=RESTCLIENTS_RUN_MODE)

GWS_CONF = dict(HOST=RESTCLIENTS_GWS_HOST,
                SERVICE_NAME=RESTCLIENTS_GWS_SERVICE,
                CERT_FILE=RESTCLIENTS_IRWS_CERT_FILE,
                KEY_FILE=RESTCLIENTS_IRWS_KEY_FILE,
                CA_FILE=RESTCLIENTS_CA_BUNDLE,
                RUN_MODE=RESTCLIENTS_RUN_MODE)

if DEBUG and RESTCLIENTS_RUN_MODE == 'File':
    MIDDLEWARE_CLASSES = (['idbase.middleware.MockLoginMiddleware'] +
                          MIDDLEWARE_CLASSES)

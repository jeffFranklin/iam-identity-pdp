import os
# Django setting for personal prefs
# These can be reset in 'local_settings.py'

DEBUG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = 'set-in-local_settings'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

USER_SERVICE_NO_DEFAULT_USER = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'userservice',
    'restclients',
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

AUTHENTICATION_BACKENDS = (
     'django.contrib.auth.backends.RemoteUserBackend',
)

PDP_BASE = '/id/'
LOGIN_URL = '/id/login/'
GET_FULL_NAME_FUNCTION = 'pdp.util.get_full_name'
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_NAME = 'pdpsession'
SESSION_COOKIE_PATH = '/'
SESSION_COOKIE_SECURE = False  # False if you are using development environment
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db/db.sqlite3'),
    }
}
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# To be removed in Django > 1.8
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "idbase.context_processors.app_context")

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
                'idbase.context_processors.app_context'
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
        'restclients': {
            'handlers': ['debuglog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'idbase':{
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'pdp/static'),
)


# PWS settings
RESTCLIENTS_IRWS_DAO_CLASS = 'restclients.dao_implementation.irws.File'
RESTCLIENTS_IRWS_HOST = 'https://mango-dev.u.washington.edu:443'
RESTCLIENTS_IRWS_SERVICE_NAME = 'registry-dev'
RESTCLIENTS_IRWS_CERT_FILE = '/data/local/etc/x315.crt'
RESTCLIENTS_IRWS_KEY_FILE = '/data/local/etc/x315.key'
RESTCLIENTS_CA_BUNDLE = '/data/local/etc/cacerts.cert'
RESTCLIENTS_IRWS_MAX_POOL_SIZE = 10

RESTCLIENTS_TIMEOUT = None
# RESTCLIENTS_DAO_CACHE_CLASS = 'pdp.cache.UICache'
# import local settings
try:
    from local_settings import *
except ImportError:
    pass


APP_CONTEXTS = {
    'default': {'base_url': PDP_BASE, 'css_loads': ['pdp.css'], 'javascript_loads': ['pdp-app.js']}
}

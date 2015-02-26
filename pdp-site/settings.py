import os
# Django setting for personal prefs 
# These can be reset in 'local_settings.py'

DEBUG = False
ALLOWED_HOSTS = ['*']


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = 'set-in-local_settings'

TEMPLATE_DEBUG = False

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
    'compressor',
    'templatetag_handlebars',
    'userservice',
    # 'demoapp',
    'restclients',
    'pdp'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'uw_django.auth.middleware.RemoteUserIfExistsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mobility.middleware.DetectMobileMiddleware',
    'mobility.middleware.XMobileMiddleware',
    'userservice.user.UserServiceMiddleware',

)

ROOT_URLCONF = 'pdp-site.urls'

WSGI_APPLICATION = 'pdp-site.wsgi.application'

AUTHENTICATION_BACKENDS = (
     'django.contrib.auth.backends.RemoteUserBackend',
)

LOGIN_URL = '/pdp/login/'
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_NAME = 'pdpsession'
SESSION_COOKIE_PATH = '/pdp/'
SESSION_COOKIE_SECURE = True  # False if you are using development environment
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
            'filename': os.path.join(BASE_DIR, 'process.log'),
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

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

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
    'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# PWS settings
RESTCLIENTS_PWS_DAO_CLASS = 'restclients.dao_implementation.pws.File'
RESTCLIENTS_PWS_HOST = 'https://ws.admin.washington.edu:443'
RESTCLIENTS_PWS_CERT_FILE = '/data/local/etc/x315.crt'
RESTCLIENTS_PWS_KEY_FILE = '/data/local/etc/x315.key'
RESTCLIENTS_CA_BUNDLE = '/data/local/etc/cacerts.cert'
RESTCLIENTS_PWS_MAX_POOL_SIZE = 10

RESTCLIENTS_TIMEOUT = None
# RESTCLIENTS_DAO_CACHE_CLASS = 'pdp.cache.UICache'

# import local settings
try:
    from local_settings import *
except ImportError:
    pass


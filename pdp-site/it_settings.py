from settings import *

MIDDLEWARE_CLASSES = [x for x in MIDDLEWARE_CLASSES
                      if x != 'django.middleware.csrf.CsrfViewMiddleware']
LOGGING = {}

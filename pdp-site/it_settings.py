from settings import *

MIDDLEWARE_CLASSES = tuple(x for x in MIDDLEWARE_CLASSES
                           if x != 'django.middleware.csrf.CsrfViewMiddleware')

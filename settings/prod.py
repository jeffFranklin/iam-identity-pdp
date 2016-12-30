from .dev import *

DEBUG = False
ALLOWED_HOSTS = ['identity.uw.edu']
COMPRESS_ENABLED = True
PROFILE_IMPERSONATORS_GROUP = None  # Turn off for prod
IRWS_URL = 'https://mango.u.washington.edu:646/registry'

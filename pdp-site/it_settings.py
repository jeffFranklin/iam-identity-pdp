"""
Integration test settings.
"""
from settings import *
import json


LOGIN_URL = '/id/mocklogin'  # Hide the LOGIN_URL from shib
MIDDLEWARE_CLASSES.insert(0, 'idbase.middleware.MockLoginMiddleware')
RESTCLIENTS_IRWS_HOST = 'https://mango-eval.u.washington.edu:646'
RESTCLIENTS_IRWS_SERVICE_NAME = 'registry-eval'

if RESTCLIENTS_IRWS_DAO_CLASS == 'restclients.dao_implementation.irws.File':
    # if we're mocking then stuff the cache for our users under test.
    from restclients.dao_implementation.irws import File
    File._cache.update({
        '/{service}/v1/name/uwnetid=idtest55'.format(
            service=RESTCLIENTS_IRWS_SERVICE_NAME): json.dumps({
                'name': [{
                    'validid': '123',
                    'formal_fname': 'DWIGHT', 'formal_sname': 'ADAMS'}
                ]})
    })
LOGGING = None

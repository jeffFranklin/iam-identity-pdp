"""
WSGI config exposes the WSGI callable as a module-level variable named
``application``.

IAM customization to set the environment according to file name
(wsgi_dev.py would use DJANGO_SETTINGS_MODULE=settings.dev, etc).

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""
import os
import re
from django.core.wsgi import get_wsgi_application

re_match = re.match(r'wsgi_(\w+).py', os.path.basename(__file__))
env_settings = '.' + re_match.group(1) if re_match else ''
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings" + env_settings)
os.environ.setdefault("DJANGO_FILE_LOGGING", "1")

application = get_wsgi_application()

from django.conf.urls import url
from django.conf import settings

from pdp.views.page import index
from pdp.views.api.name import Name
from pdp.views.api.identity import Publish
from idbase.api import LoginStatus
from idbase.views import login


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^login', login),
    url(r'^api/loginstatus$', LoginStatus(login_required=False).run),
    url(r'^api/name$', Name().run, name='name'),
    url(r'^api/publish$', Publish().run)
]


if (settings.DEBUG and
        'idbase.middleware.MockLoginMiddleware' in settings.MIDDLEWARE_CLASSES):
    urlpatterns.append(url(r'^mocklogin', login))
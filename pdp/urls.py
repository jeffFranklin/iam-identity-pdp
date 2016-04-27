from django.conf.urls import url
from django.conf import settings

from pdp.views import index, cascade
from pdp.api import Name, Publish, Profile
from idbase.api import LoginStatus
from idbase.views import login, logout


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^cascade/$', cascade, name='new cascade page'),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^api/loginstatus$', LoginStatus(login_required=False).run),
    url(r'^api/name$', Name().run, name='name'),
    url(r'^api/publish$', Publish().run),
    url(r'^api/profile/$', Profile().run)
]


if (settings.DEBUG and
        'idbase.middleware.MockLoginMiddleware' in
        settings.MIDDLEWARE_CLASSES):
    urlpatterns.append(url(r'^mocklogin', login))

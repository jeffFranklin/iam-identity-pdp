from django.conf.urls import url, include
from django.conf import settings

from pdp.views import index
from pdp.api import Name, Publish, Profile
from idbase.api import LoginStatus
from idbase.views import login, logout


profile_urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^cascade/$', index, name='new cascade page'),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^api/loginstatus$', LoginStatus(login_required=False).run),
    url(r'^api/name/(?P<netid>[^/]*)$', Name().run, name='name'),
    url(r'^api/publish/(?P<netid>[^/]*)$', Publish().run),
    url(r'^api/profile/(?P<netid>[^/]*)$', Profile().run)
]

if settings.USE_MOCK_LOGIN:
    profile_urlpatterns.append(url(r'^mocklogin', login))


urlpatterns = [
    url(r'profile/', include(profile_urlpatterns)),
    url(r'', include(profile_urlpatterns))
]

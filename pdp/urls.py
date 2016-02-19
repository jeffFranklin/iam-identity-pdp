from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from pdp.views.api.name import Name
from pdp.views.api.identity import Publish
from idbase.api import LoginStatus
from idbase.views import login


urlpatterns = patterns(
    'pdp.views',
    url(r'^$', 'page.index', name='home'),
    url(r'^login$', login),
    url(r'^api/loginstatus$', LoginStatus(login_required=False).run),
    url(r'^api/name$', Name().run, name='name'),
    url(r'^api/publish$', Publish().run)
)

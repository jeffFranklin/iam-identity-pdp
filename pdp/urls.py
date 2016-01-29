from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from pdp.views.api.name import Name
from pdp.views.api.identity import Publish
from idbase.api import Login


urlpatterns = patterns(
    'pdp.views',
    url(r'^$', 'page.index', name='home'),
    url(r'^login/', 'page.login', name='login'),
    url(r'^api/name$', login_required(Name().run), name='name'),
    url(r'^api/publish$', Publish().run),
    url(r'^api/login$', Login().run)
)

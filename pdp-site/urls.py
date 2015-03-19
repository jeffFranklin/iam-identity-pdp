from django.conf.urls import patterns, include, url
from django.contrib import admin

from pdp.views.page import login_required
from pdp.views.api.name import Name
from pdp.views.api.identity import Publish


urlpatterns = patterns(
    'pdp.views',
    url(r'^$', 'page.index'),
    url(r'login/', 'page.login', name='login'),
    url(r'api/name$', Name().run),
    url(r'api/identity/publish$', Publish().run),
)

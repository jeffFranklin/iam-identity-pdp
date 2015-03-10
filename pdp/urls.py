from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from pdp.views.api.name import Name

urlpatterns = patterns(
    'pdp.views',
    url(r'^$', 'page.index', name='home'),
    url(r'^login/', 'page.login', name='login'),
    url(r'^api/name$', login_required(Name().run), name='name'),
)

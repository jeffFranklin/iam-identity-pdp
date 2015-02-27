from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
import pdp.views.api

urlpatterns = patterns(
    'pdp.views',
    url(r'^$', 'page.index', name='home'),
    url(r'^login/', 'page.login', name='login'),
    url(r'^api/attr/', login_required(pdp.views.api.Attr().run), name='spud'),
    url(r'^api/pref-name$', pdp.views.api.PrefNameView.as_view(),
        name='pref-name'),
)

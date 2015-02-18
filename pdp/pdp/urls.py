from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from views.api.attr import Attr

urlpatterns = patterns(
    '',
    url(r'^$', 'views.page.index'),
    url(r'login/', 'views.page.login'),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'attr/', login_required(Attr().run), name='spud'),
)

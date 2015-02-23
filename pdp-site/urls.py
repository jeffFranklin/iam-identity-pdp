from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^$', 'pdp.views.page.index'),
    url(r'pdp/', include('pdp.urls')),
)

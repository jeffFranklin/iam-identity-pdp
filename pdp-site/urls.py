from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^id/', include('pdp.urls')),  # we're trending towards /id
    url(r'^pdp/', include('pdp.urls')),
    url(r'', include('pdp.urls')),  # make the root equivalent to pdp/
)

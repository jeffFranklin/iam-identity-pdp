from django.conf.urls import include, url


urlpatterns = [
    url(r'^id/', include('pdp.urls')),  # we're trending towards /id
    url(r'^pdp/', include('pdp.urls')),
    url(r'', include('pdp.urls')),  # make the root equivalent to pdp/
]

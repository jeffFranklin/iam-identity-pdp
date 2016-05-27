from django.conf.urls import include, url


urlpatterns = [
    url(r'^profile/', include('pdp.urls')),
    url(r'', include('pdp.urls')),  # make the root equivalent to profile/
]

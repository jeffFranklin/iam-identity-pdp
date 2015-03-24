from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'authz_group.views.demo_page'),
    url(r'^/rest/v1/groups$', 'authz_group.views.group_data'),
)

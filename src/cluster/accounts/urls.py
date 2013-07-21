from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^login/$', 'cluster.accounts.views.login', name='login'),
)

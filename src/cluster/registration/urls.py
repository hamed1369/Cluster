from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'cluster.registration.views.index', name='index'),
)

from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'khooshe.registration.views.index', name='index'),
)

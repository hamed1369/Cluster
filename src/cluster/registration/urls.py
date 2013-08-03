from django.conf.urls import patterns, url

urlpatterns = patterns('cluster.registration.views',
                       # url(r'^$', '.index', name='index'),
                       url(r'^register/$', 'register', name='register'),
                       url(r'^register/(?P<cluster_id>\d+)/$', 'register'), )

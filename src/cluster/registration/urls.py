from django.conf.urls import patterns, url

urlpatterns = patterns('cluster.registration.views',
                       # url(r'^$', '.index', name='index'),
                       url(r'^register/$', 'register', name='register'),
                       url(r'^register/(?P<cluster_id>\d+)/$', 'register_member'),
                       url(r'^arbiter_register/$', 'arbiter_register', name='arbiter_register'),
                       url(r'^en/register/$', 'international_register', name='international_register'),
                       url(r'^arbiter_edit/$', 'arbiter_edit', name='arbiter_edit'),

)
